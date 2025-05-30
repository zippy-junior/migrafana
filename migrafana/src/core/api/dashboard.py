from typing import Optional
from core.api.base import GrafanaBaseManager


class GrafanaDashboardManager(GrafanaBaseManager):
    """Manager for Grafana dashboards using grafana-client"""

    def get_by_uid(self, uid: str) -> Optional[dict]:
        """Get dashboard by UID"""
        dashboard_json = self.connections.master.dashboard.get_dashboard(uid)
        return dashboard_json

    def create(self, data: dict) -> dict:
        """Create a new dashboard"""
        if not self.connections.slaves:
            return self.connections.master.dashboard.create_dashboard(
                dashboard=data
            )
        else:
            for slave in self.connections.slaves:
                slave.dashboard.create_dashboard(
                    dashboard=data
                )
            return

    def update(self, data: dict) -> dict:
        if self.connections.slaves:
            for slave in self.connections.slaves:
                slave.dashboard.update_dashboard(
                    dashboard=data
                )
            return
        else:
            return self.connections.master.dashboard.update_dashboard(
                dashboard=data
            )

    def delete(self, uid: str) -> dict:
        """Delete dashboard by UID"""
        if self.connections.slaves:
            for slave in self.connections.slaves:
                slave.dashboard.delete_dashboard(
                    uid
                )
            return
        else:
            return self.connections.master.dashboard.delete_dashboard(
                uid
            )

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
