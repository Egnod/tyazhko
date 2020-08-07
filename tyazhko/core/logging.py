import logging

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            logging.getLevelName(level), record.getMessage()
        )


def set_logging():
    _logger = logging.getLogger()
    _logger.addHandler(InterceptHandler())
