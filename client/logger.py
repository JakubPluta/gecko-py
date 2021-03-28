import logging, sys


def create_logger(name):
    logger = logging.getLogger(name=name)
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    log_fmt = '[%(levelname)s] - %(asctime)s - %(process)d - %(name)s - %(funcName)s:%(lineno)d - %(message)s'
    default_formatter = logging.Formatter(log_fmt)
    stream_handler.setFormatter(default_formatter)
    logger.addHandler(stream_handler)
    return logger
