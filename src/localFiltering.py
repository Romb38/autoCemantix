import pickle
import re
import pandas as pd
import logging
from gensim.models import KeyedVectors

def filter_model_locally(model, old_invalid_words, glossary_path, logger):
    """
    Filter the Word2Vec model by removing invalid, plural, conjugated,
    or otherwise unwanted words based on the glossary provided in the config.

    :param KeyedVectors model: Model to filter
    :param set invalid_words: Already found invalid words
    :param str glossary_path: Path to glossary as defined in README.md
    :param logging.Logger logger: Logger
    :returns: Dictionary containing all invalids words founded
    :rtype: set
    """

    logger.info(f"Loading glossary from {glossary_path}")
    if glossary_path is None:
        logger.error("Glossary needs to be defined in configuration")
        return None
    df = pd.read_csv(glossary_path, sep="\t")

    def is_valid_word(word):
        if len(word) < 2:
            return False
        if not word[0].isalnum():
            return False
        if not word.replace("-","").isalnum():
            if word == "détention":
                print("Detected")
            return False
        if word == "détention":
            print("ok")
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

    invalid_words = set()
    total_words = len(model.key_to_index)
    for i, word in enumerate(model.key_to_index):
        if i % (total_words // 100) == 0:
            logger.info(f"Progress: {i/total_words*100:.2f}% ({i}/{total_words})")

        if not (word in old_invalid_words):
            continue
        if exists(word):
            continue
        if is_valid_word(word):
            continue
        if not is_plural(word):
            continue
        if not is_conjugated(word):
            continue

        invalid_words.add(word)

    logger.info(f"{len(invalid_words)} invalid words found")
    logger.info(f"{total_words - len(invalid_words)} valid words after filtering")

    return invalid_words
