import logging
from logging.config import dictConfig

from core.journaling.config import Settings

StreamHandler = "logging.StreamHandler"

settings = Settings()

internal_logger = logging.getLogger("migrafana")
stdout_logger = logging.getLogger("stdout_log")

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "defaultFormatter": {"format": "%(asctime)s %(name)s %(levelname)s %(message)s"},
        "consoleFormatter": {"format": "%(message)s"}
    },
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["internalDefault"],
            "propagate": False,
        },
        "migrafana": {
            "level": settings.LOG_LEVEL,
            "propagate": False,
            "handlers": ["internalDefault"],
        },
        "stdout_log": {
            "level": "INFO",
            "propagate": False,
            "handlers": ["consoleDefault"],
        },
    },
    "handlers": {
        "internalDefault": {
            "class": StreamHandler,
            "level": "DEBUG",
            "formatter": "defaultFormatter",
            "stream": "ext://sys.stdout",
        },
        "consoleDefault": {
            "class": StreamHandler,
            "level": "INFO",
            "formatter": "consoleFormatter",
            "stream": "ext://sys.stdout"
        }
    },
}

dictConfig(logging_config)
