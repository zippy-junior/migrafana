from grafana_client import GrafanaApi

from api.models import GrafanaConnection, GrafanaCreds


class GrafanaBaseManager():

    def __init__(self, url, creds):
        self.connection = self.connect(url, creds)

    @staticmethod
    def connect(url, creds: GrafanaCreds) -> GrafanaConnection:
        grafana_inst = GrafanaApi.from_url(
            url=url,
            credential=(creds.login, creds.password)  # Tuple of (user, pass)
        )
        try:
            grafana_inst.connect()
            return GrafanaConnection(instance=grafana_inst)
        except Exception as e:
            return GrafanaConnection(error=e)
