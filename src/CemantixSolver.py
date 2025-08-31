import logging
import time
import re
import heapq
import requests
import pickle
from requests.structures import CaseInsensitiveDict
from gensim.models import KeyedVectors
import logging
from src.configLoader import setup_logging
import os
import time
from dotenv import load_dotenv

class CemantixSolver:
    
    def __init__(self, config):
        load_dotenv()
        setup_logging(config["log_level"], config["log_file"])
        self.logger = logging.getLogger(__name__)

        self.invalid_words_file = config["invalid_dict_path"]
        self.invalid_words = self.__load_invalid_words()

        self.start_words = config["start_words"]
        self.beam_size = config["beam_size"]
        self.topn = config["topn"]
        self.api_delay = config["api_delay"]
        self.model_path = config["model_path"]
        self.schema = config["schema"]
        self.url = config["url"]
        self.user_agent = config["user_agent"]
        self.content_type = config["content_type"]
        self.max_retries = config["max_retries"]

        self.headers = CaseInsensitiveDict({
            "Content-Type": self.content_type,
            "Host": self.url,
            "Origin": f"{self.schema}://{self.url}",
            "referrer": f"{self.schema}://{self.url}/",
            "User-Agent": self.user_agent
        })
        self.similar_cache = {}


    def __load_invalid_words(self):
        try:
            with open(self.invalid_words_file, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return set()

    def __save_invalid_words(self):
        with open(self.invalid_words_file, "wb") as f:
            pickle.dump(self.invalid_words, f)

    def __mark_invalid(self, word):
        self.invalid_words.add(word)
        self.__save_invalid_words()

    def __get_puzzle_number(self):
        self.logger.info("Getting puzzle number")
        resp = requests.get(f"{self.schema}://{self.url}", headers=self.headers, timeout=30)
        if resp.status_code == 200:
            match = re.search(r'data-puzzle-number="(\d+)"', resp.text)
            if match:
                puzzle_number = int(match.group(1))
                self.logger.info("Puzzle number: %d", puzzle_number)
                return puzzle_number
        self.logger.error("No puzzle number found")
        return None

    def __get_score(self, word, day):
        for attempt in range(self.max_retries):
            try:
                url = f"{self.schema}://{self.url}/score?n={day}"
                resp = requests.post(url, headers=self.headers, data=f"word={word}".encode("utf-8"), timeout=30)
                resp_json = resp.json()
                if resp.status_code != 200:
                    return None
                if 'e' in resp_json:
                    self.logger.warning("Word '%s' error: %s", word, resp_json['e'])
                    self.__mark_invalid(word)
                    return None
                return resp_json['s']
            except Exception as e:
                self.logger.warning("Error fetching score for '%s': %s (retry %d/%d)", word, e, attempt+1, self.max_retries)
                time.sleep(self.api_delay)
        return None

    def __log_and_notify(self, word, exec_time):
        msg = f"Mot trouvé: {word}, Requêtes: {self.request_count}, Temps: {exec_time:.2f} sec"
        self.logger.info("Résultat final → %s", msg)
        token = os.getenv("NTFY_TOKEN")
        subject = os.getenv("NTFY_SUBJECT")
        os.system(f'ntfy publish --token {token} https://ntfy.standouda.fr/{subject} "{msg}"')
        
    def __filter_dictionnary(self,model):
        self.logger.info("Remove invalid words from model")
        with open(self.invalid_words_file, "rb") as f:
            invalid_words = pickle.load(f)
        invalid_words = set(invalid_words)
        valid_words = [word for word in model.key_to_index if word not in invalid_words]
        valid_vectors = [model[word] for word in valid_words]
        filtered_model = KeyedVectors(vector_size=model.vector_size)
        filtered_model.add_vectors(valid_words, valid_vectors)
        filtered_model.save_word2vec_format(self.model_path, binary=True)
        return


    def solve(self):
        self.logger.info("Solver started")
        
        start_time = time.time()
        self.request_count = 0
        
        self.logger.info("Loading model '%s'", self.model_path)
        model = KeyedVectors.load_word2vec_format(self.model_path, binary=True, unicode_errors="ignore")
        self.logger.info("Model loaded")

        day = self.__get_puzzle_number()
        if day is None:
            return None

        tested = set()
        beam = []

        # Initialisation
        for w in self.start_words:
            if w in self.invalid_words:
                continue
            self.request_count += 1 
            score = self.__get_score(w, day)
            if score is not None:
                tested.add(w)
                heapq.heappush(beam, (-score, w))
                self.logger.info("Initial: %s → %.4f", w, score)

        if not beam:
            self.logger.error("No valid starting words")
            return None

        best_score, best_word = -beam[0][0], beam[0][1]

        while best_score < 1.0:
            new_candidates = []

            for _ in range(min(self.beam_size, len(beam))):
                _, word = heapq.heappop(beam)
                if word not in model:
                    continue

                if word in self.similar_cache:
                    neighbors = self.similar_cache[word]
                else:
                    neighbors = model.most_similar(word, topn=self.topn)
                    self.similar_cache[word] = neighbors

                for neigh, _ in neighbors:
                    if neigh in tested or neigh in self.invalid_words:
                        continue
                    self.request_count += 1 
                    score = self.__get_score(neigh, day)
                    if score is None:
                        continue
                    tested.add(neigh)
                    heapq.heappush(new_candidates, (-score, neigh))

                    if score > best_score:
                        best_score, best_word = score, neigh
                        self.logger.info("New best: %s → %.4f", neigh, score)
                        if best_score >= 1.0:
                            self.logger.info("Solution found: %s → %.4f", best_word, best_score)
                            break

                    time.sleep(self.api_delay)
            if best_score >= 1.0:
                break

            for item in new_candidates:
                heapq.heappush(beam, item)

            # Garder seulement les top BEAM_SIZE
            beam = heapq.nsmallest(self.beam_size, beam)

            if not new_candidates:
                self.logger.warning("No new candidates found, stopping.")
                break

        self.logger.info("Solving ended")
        
        exec_time = time.time() - start_time
        self.__log_and_notify(best_word, exec_time)
        self.__filter_dictionnary(model)
        
        return best_word, best_score

