##
# @file CemantixSolver.py
# @brief Contains the CemantixSolver class to solve the Cemantix word puzzle game.
#
# This module implements an automatic solver using a Word2Vec model and a beam search
# strategy to guess the hidden word by interacting with the Cemantix API.

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
    """
    @brief Automatic solver for the Cemantix word game.

    This solver uses a Word2Vec model and a beam search strategy
    to guess the hidden word by querying the Cemantix API for similarity scores.
    """

    def __init__(self, config):
        """
        @brief Initializes the solver with the provided configuration.

        @param config Dictionary containing the following keys:
            - log_level: Logging verbosity level.
            - log_file: Path to the log file.
            - invalid_dict_path: Path to the pickle file with invalid words.
            - start_words: List of seed words for initialization.
            - beam_size: Number of best candidates to keep at each iteration.
            - topn: Number of similar words to retrieve from the model.
            - api_delay: Delay (in seconds) between API requests.
            - model_path: Path to the Word2Vec model.
            - schema: HTTP or HTTPS.
            - url: Domain name of the Cemantix website.
            - user_agent: User-Agent header for HTTP requests.
            - content_type: Content-Type for HTTP POST requests.
            - max_retries: Maximum number of retries for failed API calls.
        """
    
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
        """
        @brief Loads the set of invalid words from the pickle file.

        @return A set of invalid words if the file exists, otherwise an empty set.
        """

        try:
            with open(self.invalid_words_file, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return set()

    def __save_invalid_words(self):
        """
        @brief Saves the current set of invalid words to the pickle file.
        """
        with open(self.invalid_words_file, "wb") as f:
            pickle.dump(self.invalid_words, f)

    def __mark_invalid(self, word):
        
        """
        @brief Adds a word to the invalid words set and persists the update.

        @param word The word to be marked as invalid.
        """

        self.invalid_words.add(word)
        self.__save_invalid_words()

    def __get_puzzle_number(self):
        """
        @brief Fetches the current day's puzzle number from the Cemantix website.

        @return The puzzle number as an integer if found, otherwise None.
        """


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
        """
        @brief Sends a word to the API and retrieves its similarity score.

        @param word The word to test.
        @param day The puzzle number for which to retrieve the score.

        @return The similarity score (float between 0.0 and 1.0), or None if the request failed or word is invalid.
        """

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

        """
        @brief Sends a notification when the solution is found.

        Uses the ntfy notification service.

        @param word The found word (the solution).
        @param exec_time Execution time in seconds.
        """

        msg = f"Mot trouvé: {word}, Requêtes: {self.request_count}, Temps: {exec_time:.2f} sec"
        self.logger.info("Résultat final → %s", msg)
        token = os.getenv("NTFY_TOKEN")
        subject = os.getenv("NTFY_SUBJECT")
        ntfyUrl = os.getenv("NTFY_URL")
        if token and subject:
            os.system(f'ntfy publish --token {token} {NTFY_URL}/{subject} "{msg}"')
        
    def __filter_dictionnary(self,model):
        """
        @brief Filters the Word2Vec model by removing invalid words and saves the updated model.

        @param model The original Word2Vec model to filter.
        """
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


    def solve(self, day=None):
        """
        @brief Starts solving the Cemantix puzzle using beam search and a Word2Vec model.

        @param day (Optional) Puzzle number to solve. If None, the current day's puzzle will be used.

        @return A tuple (best_word, best_score) where:
            - best_word: The guessed solution (str).
            - best_score: Its similarity score (float, should be 1.0 if solved),
            or None if the puzzle could not be solved.
        """
        self.logger.info("Solver started")
        
        start_time = time.time()
        self.request_count = 0
        
        self.logger.info("Loading model '%s'", self.model_path)
        model = KeyedVectors.load_word2vec_format(self.model_path, binary=True, unicode_errors="ignore")
        self.logger.info("Model loaded")
        
        if day is None:
            day = self.__get_puzzle_number()
            if day is None:
                return None
        print(day)
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

            beam = heapq.nsmallest(self.beam_size, beam)

            if not new_candidates:
                self.logger.warning("No new candidates found, stopping.")
                break

        self.logger.info("Solving ended")
        
        exec_time = time.time() - start_time
        self.__log_and_notify(best_word, exec_time)
        self.__filter_dictionnary(model)
        
        return best_word, best_score

