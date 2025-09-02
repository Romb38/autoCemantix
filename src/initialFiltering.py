##
# @file initialFiltering.py
# @brief Module to initally filter model to remove plural, conjugated and previously founded invalid words

import pickle
import re
import pandas as pd
import logging
from gensim.models import KeyedVectors
from src.configLoader import setup_logging

def filter_model_from_config(cfg):
    """
    Filter the Word2Vec model by removing invalid, plural, conjugated,
    or otherwise unwanted words based on the glossary provided in the config.

    :param dict cfg: Configuration dictionary containing the following keys:
        - model_path (str): Path to the Word2Vec model file.
        - invalid_dict_path (str): Path to the pickle file with invalid words.
        - glossary (str): Path to the TSV glossary file.
        - log_level (str): Logging level (e.g., 'INFO').
        - log_file (str or None): Logging output file (optional).
    :returns: None
    """

    setup_logging(cfg.get("log_level", "INFO"), cfg.get("log_file", None))
    logger = logging.getLogger(__name__)

    logger.info(f"Loading glossary from {cfg['glossary']}")
    if cfg["glossary"] is None:
        logger.error("Glossary needs to be defined in configuration")
        return None
    df = pd.read_csv(cfg["glossary"], sep="\t")

    def is_valid_word(word):
        if len(word) < 2:
            return False
        if not word[0].isalnum():
            return False
        if not re.match(r'^[a-zA-Z0-9-]*$', word):
            return False
        return True

    def is_plural(word):
        word_data = df[df['ortho'] == word]
        if not word_data.empty:
            return word_data.iloc[0]['nombre'] == 'p'
        return False

    def is_conjugated(word):
        word_data = df[df['ortho'] == word]
        if not word_data.empty:
            cgram = word_data.iloc[0]['cgram']
            if type(cgram) != float:
                return 'VER' in cgram or 'AUX' in cgram
        return False

    def exists(word):
        word_data = df[df['ortho'] == word]
        return not word_data.empty

    logger.info(f"Loading model from {cfg['model_path']}")
    model = KeyedVectors.load_word2vec_format(cfg["model_path"], binary=True, unicode_errors="ignore")

    try:
        with open(cfg["invalid_dict_path"], "rb") as f:
            invalid_words = pickle.load(f)
            logger.info(f"Loaded {len(invalid_words)} invalid words.")
    except (FileNotFoundError, EOFError):
        invalid_words = set()
        logger.warning("No invalid words file found, starting with empty set.")

    filtered_words = {}
    total_words = len(model.key_to_index)

    for i, word in enumerate(model.key_to_index):
        if i % (total_words // 100) == 0:
            logger.info(f"Progress: {i/total_words*100:.2f}% ({i}/{total_words})")

        if word in invalid_words:
            continue
        if not exists(word):
            continue
        if not is_valid_word(word):
            continue
        if is_plural(word):
            continue
        if is_conjugated(word):
            continue

        filtered_words[word] = model[word]

    logger.info(f"{len(filtered_words)} valid words after filtering")

    filtered_model = KeyedVectors(vector_size=model.vector_size)
    filtered_model.add_vectors(list(filtered_words.keys()), list(filtered_words.values()))

    filtered_model.save_word2vec_format(cfg["model_path"], binary=True)
    logger.info(f"Filtered model saved to {cfg['model_path']}")
