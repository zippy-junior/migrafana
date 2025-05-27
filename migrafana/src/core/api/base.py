from grafana_client import GrafanaApi

from api.models import GrafanaConnection, GrafanaConfig, GrafanaConnectionError

def connect(conf: GrafanaConfig):
    grafana_inst = GrafanaApi.from_url(
        url=conf.url,
        credential=(conf.creds.login, conf.creds.password)  # Tuple of (user, pass)
    )
    try:
        grafana_inst.connect()
        return GrafanaConnection(instance=grafana_inst)
    except Exception as e:
        return GrafanaConnection(error=e)


class GrafanaBaseManager():

    def __init__(self):
        self.connection = None

    @classmethod
    def new(cls, conf: GrafanaConfig) -> GrafanaConnection:
        connection: GrafanaConnection = connect(conf)
        if connection.error:
            logger.error()
            raise GrafanaConnectionError

    