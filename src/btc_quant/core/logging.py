import logging

def get_logger(name="btc_quant"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    return logger

