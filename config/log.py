import logging
from datetime import datetime
from logging.config import dictConfig
from pydantic import BaseModel

class LogConfig(BaseModel):
    LOGGER_NAME: str = "python-service"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            # "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "camspay-service": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
    }


dictConfig(LogConfig().dict())
logger = logging.getLogger("python-service")
fh = logging.FileHandler('logs/python-service-{}.log'.format(datetime.now().strftime('%Y_%m_%d')))
formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)04d | %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)