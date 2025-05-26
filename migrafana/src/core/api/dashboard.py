from typing import Dict, List, Optional

from core.api.base import GrafanaAPIClient
from core.json_parser.parser import apply_patch


class GrafanaDashboardManager:
    """Manager for Grafana dashboards using grafana-client"""

    def __init__(self, api_client: GrafanaAPIClient):
        self.api = api_client

    def get_dashboard(self, uid: str) -> dict:
        """Get dashboard by UID"""
        dashboard_json = self.api.client.dashboard.get_dashboard(uid)
        return dashboard_json

    def create_dashboard(self, dashboard: dict) -> Dict:
        """Create a new dashboard"""
        return self.api.client.dashboard.update_dashboard(
            dashboard=dashboard
        )

    def update_dashboard(self, dashboard: dict) -> Dict:
        """Update existing dashboard"""
        return self.api.client.dashboard.update_dashboard(
            dashboard=dashboard
        )

    def delete_dashboard(self, uid: str) -> Dict:
        """Delete dashboard by UID"""
        return self.api.client.dashboard.delete_dashboard(uid)

    def search_dashboards(self, query: str = "", tag: str = "") -> List[Dict]:
        """Search for dashboards"""
        params = {}
        if query:
            params['query'] = query
        if tag:
            params['tag'] = tag
        return self.api.client.search.search_dashboards(params=params)

    def transfer_datasource(
        self,
        uid: str,
        patch_operations: list[dict],
        target_service: Optional['GrafanaDashboardManager'] = None
    ) -> Dict:
        dashboard = self.get_dashboard(uid)
        patched = apply_patch(dashboard['dashboard'], patch_operations)
        dashboard['dashboard'] = patched
        target = target_service if target_service else self
        return target.update_dashboard(uid, dashboard)
