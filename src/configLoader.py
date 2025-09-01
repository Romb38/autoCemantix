##
# @file configLoader.py
# @brief Module to load configuration and set up logging.

import configparser
import logging

def load_config(filename="src/ressources/config.ini"):
    """
    @brief Loads configuration values from a .ini file.

    This function reads the "GENERAL" section of the configuration file
    and converts the values to appropriate Python types.

    @param filename Path to the configuration file. Defaults to "src/ressources/config.ini".

    @return A dictionary containing the configuration values, including:
        - start_words: List of seed words (list of str).
        - beam_size: Beam width for search (int).
        - topn: Number of similar words to retrieve (int).
        - api_delay: Delay between API requests in seconds (float).
        - model_path: Path to the Word2Vec model (str).
        - invalid_dict_path: Path to the invalid words pickle file (str).
        - schema: URL schema (http/https) (str).
        - url: Domain of the Cemantix server (str).
        - user_agent: User-Agent string for HTTP requests (str).
        - content_type: HTTP request content type (str).
        - max_retries: Maximum number of retries for requests (int).
        - log_level: Logging level (str).
        - glossary_path : Glossary needed to filter words from model (str)
        - log_file: Path to the log file (str).
    """

    parser = configparser.ConfigParser()
    parser.read(filename)

    cfg = parser["GENERAL"]

    # Conversion avec types corrects
    config = {
        "start_words": [w.strip() for w in cfg.get("start_words", "").split(",")],
        "beam_size": cfg.getint("beam_size", 5),
        "topn": cfg.getint("topn", 20),
        "api_delay": cfg.getfloat("api_delay", 1.0),
        "model_path": cfg.get("model_path", "frWac.bin"),
        "invalid_dict_path": cfg.get("invalid_dict_path", "invalid_words.pkl"),
        "schema": cfg.get("schema", "https"),
        "url": cfg.get("url", "cemantix.certitudes.org"),
        "user_agent": cfg.get("user_agent", ""),
        "content_type": cfg.get("content_type", "application/x-www-form-urlencoded"),
        "max_retries": cfg.getint("max_retries", 3),
        "log_level": cfg.get("log_level", "INFO").upper(),
        "log_file": cfg.get("log_file", "").strip(),
        "glossary": cfg.get("glossary_path", None)
    }

    return config


def setup_logging(log_level: str, log_file: str):
    """
    @brief Sets up global logging based on configuration.

    Initializes the logging system either to a file (if provided)
    or to the console. Sets the logging format and level accordingly.

    @param log_level The logging level (e.g., "INFO", "DEBUG", "ERROR").
    @param log_file Path to the log file. If empty, logs are printed to stdout.
    """

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    handlers = []
    if log_file:
        handlers.append(logging.FileHandler(log_file, mode="a", encoding="utf-8"))
    else :
        handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=numeric_level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        handlers=handlers
    )
