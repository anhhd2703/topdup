import logging
from ._config import LOG_FILE


def get_logger(name, f_name=LOG_FILE):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formater = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fhanler = logging.FileHandler(f_name, 'a+', encoding='utf-8')
    fhanler.setFormatter(formater)
    fhanler.setLevel(logging.DEBUG)
    logger.addHandler(fhanler)
    return logger
