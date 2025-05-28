from core.api.base import GrafanaBaseManager


class GrafanaDashboardManager(GrafanaBaseManager):
    """Manager for Grafana dashboards using grafana-client"""

    def get_by_uid(self, uid: str) -> dict:
        """Get dashboard by UID"""
        dashboard_json = self.connection.instance.dashboard.get_by_uid(uid)
        return dashboard_json

    def create(self, instance: dict) -> dict:
        """Create a new dashboard"""
        return self.connection.instance.dashboard.update(
            dashboard=instance
        )

    def update(self, instance: dict) -> dict:
        """Update existing dashboard"""
        return self.connection.instance.dashboard.update(
            dashboard=instance
        )

    def delete(self, uid: str) -> dict:
        """Delete dashboard by UID"""
        return self.connection.instance.dashboard.delete(uid)

    def search(self, query: str = "", tag: str = "") -> dict:
        """Search for dashboards"""
        params = {}
        if query:
            params['query'] = query
        if tag:
            params['tag'] = tag
        params['type_'] = "dash-db"
        return self.connection.instance.search.search_dashboards(**params)

    def get_all(self) -> list[dict]:
        """List all dashboards"""
        return self.search()
