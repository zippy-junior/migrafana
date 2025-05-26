from grafana_client import GrafanaApi
from core.models import GrafanaConfig


class GrafanaAPIClient:
    def __init__(self, config: GrafanaConfig):
        self.config = config
        self.client = self._initialize_client()

    def _initialize_client(self) -> GrafanaApi:
        if self.config.api_key:
            return GrafanaApi.from_url(
                url=self.config.url,
                credential=self.config.api_key
            )
        elif self.config.username and self.config.password:
            return GrafanaApi.from_url(
                url=self.config.url,
                credential=(self.config.username, self.config.password)
            )
        raise ValueError("No valid authentication method provided")

    def test_connection(self) -> bool:
        try:
            return bool(self.client.connect())
        except Exception:
            return False
