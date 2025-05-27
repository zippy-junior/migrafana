from grafana_client import GrafanaApi

from core.api.models import (GrafanaConnection,
                             GrafanaConfig,
                             GrafanaConnectionError)
from core.journaling import internal_logger as i_logger


def connect(conf: GrafanaConfig):
    grafana_inst = GrafanaApi.from_url(
        url=conf.url,
        credential=(conf.creds.login, conf.creds.password)
    )
    try:
        grafana_inst.connect()
        return GrafanaConnection(instance=grafana_inst)
    except Exception as e:
        return GrafanaConnection(error=e)


class GrafanaBaseManager():

    def __init__(self, connection: GrafanaConnection):
        self.connection = connection

    @classmethod
    def from_config(cls, conf: GrafanaConfig) -> GrafanaConnection:
        connection: GrafanaConnection = connect(conf)
        if connection.error:
            i_logger.error(connection.error)
            raise GrafanaConnectionError(connection.error)
        else:
            return cls(connection)
