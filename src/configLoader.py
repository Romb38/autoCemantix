##
# @file configLoader.py
# @brief Module to load configuration and set up logging.

import configparser
import logging
import os
import sys

def load_config(filename="src/resources/config.ini"):
    """
    Load configuration values from a .ini file.

    :param str filename: Path to the configuration file.
    :raises FileNotFoundError: If the configuration file does not exist.
    :raises KeyError: If the [GENERAL] section is missing in the configuration file.
    :returns: A dictionary containing the configuration values.
    :rtype: dict
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(f"Configuration file not found: {filename}")

    parser = configparser.ConfigParser()
    parser.read(filename)

    if "GENERAL" not in parser:
        raise KeyError(f"The section [GENERAL] is missing in {filename}. "
                       f"Found sections: {parser.sections()}")

    cfg = parser["GENERAL"]

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
        "glossary": cfg.get("glossary_path", None),
        "stats_file": cfg.get("statistics_path", None)
    }

    return config


def setup_logging(log_level: str, log_file: str):
    """
    Set up global logging based on configuration.

    :param str log_level: Logging level as a string (e.g., 'INFO', 'DEBUG').
    :param str log_file: Path to the log file. If empty, logs are output to stdout.
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    handlers = []
    if log_file:
        handlers.append(logging.FileHandler(log_file, mode="a", encoding="utf-8"))
    
    handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=numeric_level,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        handlers=handlers
    )
