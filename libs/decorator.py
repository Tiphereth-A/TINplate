import logging


def withlog(func):
    logger: logging.Logger = logging.getLogger(func.__name__)

    def inner(*args, **kwargs):
        logger.debug(rf"start running under args: {args}, kwargs: {kwargs}")
        return_val = func(*args, **kwargs, logger=logger)
        logger.debug(rf"running finished under args: {args}, kwargs: {kwargs}")
        return return_val

    return inner
