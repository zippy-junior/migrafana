from typing import Dict, List
from core.api.base import GrafanaBaseManager


class GrafanaDashboardManager(GrafanaBaseManager):
    """Manager for Grafana dashboards using grafana-client"""

    def get_dashboard(self, uid: str) -> dict:
        """Get dashboard by UID"""
        dashboard_json = self.connection.instance.dashboard.get_dashboard(uid)
        return dashboard_json

    def create_dashboard(self, dashboard: dict) -> Dict:
        """Create a new dashboard"""
        return self.connection.instance.dashboard.update_dashboard(
            dashboard=dashboard
        )

    def update_dashboard(self, dashboard: dict) -> Dict:
        """Update existing dashboard"""
        return self.connection.instance.dashboard.update_dashboard(
            dashboard=dashboard
        )

    def delete_dashboard(self, uid: str) -> Dict:
        """Delete dashboard by UID"""
        return self.connection.instance.dashboard.delete_dashboard(uid)

    def search_dashboards(self, query: str = "", tag: str = "") -> List[Dict]:
        """Search for dashboards"""
        params = {}
        if query:
            params['query'] = query
        if tag:
            params['tag'] = tag
        return self.connection.instance.search.search_dashboards(params=params)
