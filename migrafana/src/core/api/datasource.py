from typing import Dict, List, Optional, Union
from core.api.base import GrafanaBaseManager


class GrafanaDataSourceManager(GrafanaBaseManager):
    """Manager for Grafana data sources using grafana-client"""

    def get_datasource(self, uid: str) -> Dict:
        """Get data source by UID"""
        return self.connection.instance.datasource.get_datasource_by_uid(uid)

    def get_datasource_by_id(self, id: int) -> Dict:
        """Get data source by ID"""
        return self.connection.instance.datasource.get_datasource_by_id(id)

    def get_datasource_by_name(self, name: str) -> Dict:
        """Get data source by name"""
        return self.connection.instance.datasource.get_datasource_by_name(name)

    def create_datasource(self, datasource_config: Dict) -> Dict:
        """
        Create a new data source
        Args:
            datasource_config: Complete data source configuration including:
                - name: (str) Data source name
                - type: (str) Data source type (prometheus, graphite, etc.)
                - access: (str) Proxy or Direct
                - url: (str) Data source URL
                - (plus type-specific settings)
        """
        return self.connection.instance.datasource.create_datasource(datasource_config)

    def update_datasource(self, uid: str, datasource_config: Dict) -> Dict:
        """Update existing data source by UID"""
        return self.connection.instance.datasource.update_datasource_by_uid(uid, datasource_config)

    def delete_datasource(self, uid: str) -> Dict:
        """Delete data source by UID"""
        return self.connection.instance.datasource.delete_datasource_by_uid(uid)

    def delete_datasource_by_name(self, name: str) -> Dict:
        """Delete data source by name"""
        return self.connection.instance.datasource.delete_datasource_by_name(name)

    def list_datasources(self) -> List[Dict]:
        """List all data sources"""
        return self.connection.instance.datasource.list_datasources()

    def query_datasource(
        self,
        uid: str,
        query: Dict,
        time_range: Optional[Dict] = None
    ) -> Union[Dict, List]:
        """
        Query a data source directly
        Args:
            uid: Data source UID
            query: Query specific to the data source type
            time_range: Optional dict with 'from' and 'to' timestamps
        """
        return self.connection.instance.datasource.query(uid, query, time_range)

    def get_datasource_health(self, uid: str) -> Dict:
        """Check data source health by UID"""
        return self.connection.instance.datasource.health(uid)

    def get_datasource_id_by_uid(self, uid: str) -> int:
        """Get data source ID by UID"""
        return self.get_datasource(uid)["id"]

    def enable_datasource(self, uid: str) -> bool:
        """Enable a data source"""
        config = self.get_datasource(uid)
        config["isEnabled"] = True
        self.update_datasource(uid, config)
        return True

    def disable_datasource(self, uid: str) -> bool:
        """Disable a data source"""
        config = self.get_datasource(uid)
        config["isEnabled"] = False
        self.update_datasource(uid, config)
        return True

    def test_datasource(self, uid: str) -> Dict:
        """Test data source connection by UID"""
        return self.connection.instance.datasource.test_datasource_by_uid(uid)

    def get_datasource_permissions(self, uid: str) -> Dict:
        """Get data source permissions by UID"""
        return self.connection.instance.datasource.get_datasource_permissions(uid)

    def update_datasource_permissions(
        self,
        uid: str,
        permissions: Dict
    ) -> Dict:
        """Update data source permissions by UID"""
        return self.connection.instance.datasource.update_datasource_permissions(uid, permissions)