from functools import wraps
import os

from core.api.base import GrafanaBaseManager
from core.api.models import Creds, GrafanaConfig
from core.journaling import internal_logger as i_logger


def get_credentials() -> Creds:
    """Try multiple secure sources"""

    grafana_user = os.getenv('GRAFANA_USER')
    grafana_pass = os.getenv('GRAFANA_PASS')
    grafana_api_token = os.getenv('GRAFANA_API_TOKEN')
    if grafana_user and grafana_pass:
        return Creds(login=grafana_user,
                     password=grafana_pass,
                     token=grafana_api_token)

    i_logger.error("No credentials found")
    raise ValueError("No credentials found")


def using_manager(manager: GrafanaBaseManager):
    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Get src from kwargs (passed by Click)
            src = kwargs.get('src', None)
            if not src:
                raise ValueError("Source URL (--src) must be provided")

            creds = get_credentials()
            m = manager.from_config(conf=GrafanaConfig(creds=creds, url=src))

            fn(m, *args, **kwargs)
        return wrapper
    return decorator
