import logging
import time
import re
import requests
import pickle
from requests.structures import CaseInsensitiveDict
from gensim.models import KeyedVectors
from src.configLoader import setup_logging
import os
import time
from dotenv import load_dotenv
import csv
import numpy as np

class CemantixSolver:
    """
    Automatic solver for the Cemantix word game.

    This solver uses a Word2Vec model and a beam search strategy
    to guess the hidden word by querying the Cemantix API for similarity scores.
    """

    def __init__(self, config):
        """
        Initialize the solver with the provided configuration.

        :param dict config: Dictionary containing configuration keys (see configLoader).
        """
        load_dotenv()
        setup_logging(config["log_level"], config["log_file"])
        self.logger = logging.getLogger(__name__)

        if not(os.getenv("NTFY_URL") and os.getenv("NTFY_SUBJECT")):
            self.logger.info("No NTFY config found")

        self.start_words = config["start_words"]
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

        self.logger.info("Loading model '%s'", self.model_path)
        self.model = KeyedVectors.load_word2vec_format(self.model_path, binary=True, unicode_errors="ignore")
        self.logger.info("Model loaded")

    def __get_puzzle_number(self):
        """
        Fetch the current day's puzzle number from the Cemantix website.

        :returns: The puzzle number as an integer if found, otherwise None.
        :rtype: int or None
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
        Send a word to the API and retrieve its similarity score.

        :param str word: The word to test.
        :param int day: The puzzle number for which to retrieve the score.

        :returns: The similarity score (float between 0.0 and 1.0), or None if the request failed or word is invalid.
        :rtype: float or None
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
                    return None
                return resp_json['s']
            except Exception as e:
                self.logger.warning("Error fetching score for '%s': %s (retry %d/%d)", word, e, attempt+1, self.max_retries)
                time.sleep(self.api_delay)
        return None

    def __log_and_notify(self, word, score, exec_time):
        """
        Send a notification when the solution is found.

        :param str word: The found word (the solution).
        :param float exec_time: Execution time in seconds.
        """
        msg = f"Word found: {word} (score : {score}), Requests: {self.request_count}, Execution time: {exec_time:.2f} sec"
        self.logger.info("Résultat final → %s", msg)
        self.__ntfy(msg)
        return

    def __ntfy(self, msg):
        """
        Send a notification containing msg using NTFY API

        :param str msg: Message to send as notification
        :returns: None
        """

        token = os.getenv("NTFY_TOKEN")
        subject = os.getenv("NTFY_SUBJECT")
        ntfy_url = os.getenv("NTFY_URL")
        if  subject and ntfy_url:
            #os.system(f'ntfy publish --token {token} {ntfy_url}/{subject} "{msg}"')
            os.system(f'curl -H "Authorization: Bearer {token}" -d "{msg}" {ntfy_url}/{subject}')
        else :
            self.logger.error("No NTFY config found, set it up inside of .env file")


    def solve(self, day=None, ntfy=False):
        """
        Optimized Cemantix solver using NumPy vectorization to find words whose similarity
        with the start words exactly matches the expected values (within a small epsilon).

        :param int day: (Optional) Puzzle number to solve. If None, the current day's puzzle will be used.
        :param bool ntfy: (Optional) Send a notification using NTFY .env configuration
        :returns: A tuple (best_word, best_score) or None if no solution was found.
        :rtype: tuple or None
        """
        self.logger.info("Local solver started")
        start_time = time.time()
        self.request_count = 0

        word_found = None
        best_score = 0.0
        epsilon = 0.001


        if day is None:
            day = self.__get_puzzle_number()
            if day is None:
                return None

        # 1. Getting initial words score
        startings_score = {}
        for w in self.start_words:
            self.request_count += 1
            score = self.__get_score(w, day)
            if score is not None:
                if score == 1.0:
                    self.logger.info("Solution found as a starting word: %s → %.4f", w, 1.0)
                    word_found = w
                    break
                startings_score[w] = score
        self.logger.info(f"Starting scores: {startings_score}")

        if word_found:
            exec_time = time.time() - start_time
            self.logger.info(f"Execution time : {exec_time}")
            if ntfy:
                self.__log_and_notify(word_found, 1.0, exec_time)
            return word_found, 1.0

        # 2. Computing cosine similarity between all words and starting words

        # 2.1 Getting starting words vectors
        try:
            start_vectors = np.array([self.model.get_vector(w) for w in startings_score])
        except KeyError as e:
            self.logger.error(f"Start word not in model vocabulary: {e}")
            return None

        start_scores = np.array(list(startings_score.values()))

        # 2.2 Getting model vectors
        all_vectors = self.model.vectors
        all_words = self.model.index_to_key

        # Normalisation
        start_norms = np.linalg.norm(start_vectors, axis=1)
        all_norms = np.linalg.norm(all_vectors, axis=1)

        # 2.3 Computing cosine similarity
        dot_products = np.dot(start_vectors, all_vectors.T)
        norm_products = np.outer(start_norms, all_norms)
        cosine_similarities = dot_products / norm_products


        # Using cosine similarity to find candidates
        diffs = np.abs(cosine_similarities - start_scores[:, np.newaxis])
        matches = np.all(diffs <= epsilon, axis=0)
        matching_words = [all_words[i] for i, ok in enumerate(matches) if ok]

        self.logger.info(f"{len(matching_words)} matching candidates found after vectorized filtering.")

        # 3. Check if words found are correct
        for candidate in matching_words:
            self.request_count += 1
            score = self.__get_score(candidate, day)
            if score is None:
                continue
            if score == 1.0:
                self.logger.info("Solution found: %s → %.4f", candidate, 1.0)
                word_found = candidate
                best_score = 1.0
                break
            time.sleep(self.api_delay)

        exec_time = time.time() - start_time
        self.logger.info(f"Execution time : {exec_time}")
        if word_found and ntfy:
            self.__log_and_notify(word_found, best_score, exec_time)

        return word_found, best_score
