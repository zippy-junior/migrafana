from core.api.base import GrafanaBaseManager


class GrafanaDashboardManager(GrafanaBaseManager):
    """Manager for Grafana dashboards using grafana-client"""

    def get_by_uid(self, uid: str) -> dict:
        """Get dashboard by UID"""
        dashboard_json = self.connections.master.dashboard.get_by_uid(uid)
        return dashboard_json

    def create(self, instance: dict) -> dict:
        """Create a new dashboard"""
        if not self.connections.slaves:
            return self.connection.master.dashboard(
                dashboard=instance
            )
        else:
            for slave in self.connections.slaves:
                slave.dashboard.update(
                    dashboard=instance
                )
            return

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
        return self.connections.master.search.search_dashboards(**params)

    def get_all(self) -> list[dict]:
        """List all dashboards"""
        return self.search()
