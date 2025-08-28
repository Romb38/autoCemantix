import configparser
import logging

def load_config(filename="src/ressources/config.ini"):
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
        "log_file": cfg.get("log_file", "").strip()
    }

    return config


def setup_logging(log_level: str, log_file: str):
    """Configure le logger global selon la config"""
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
