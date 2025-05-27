from typing import Dict, List, Optional, Union
from core.api.base import GrafanaBaseManager


class GrafanaDataSourceManager(GrafanaBaseManager):
    """Manager for Grafana data sources using grafana-client"""

    def get_by_uid(self, uid: str) -> dict:
        """Get data source by UID"""
        return self.connection.instance.datasource.get_datasource_by_uid(uid)

    def get_by_id(self, id: int) -> dict:
        """Get data source by ID"""
        return self.connection.instance.datasource.get_datasource_by_id(id)

    def get_by_name(self, name: str) -> dict:
        """Get data source by name"""
        return self.connection.instance.datasource.get_datasource_by_name(name)

    def create(self, instance: dict) -> dict:
        """
        Create a new data source
        """
        return self.connection.instance.datasource.create_datasource(instance)

    def update(self, uid: str, instance: dict) -> dict:
        """Update existing data source by UID"""
        return self.connection.instance.datasource.update_datasource_by_uid(uid, instance)

    def delete(self, uid: str) -> dict:
        """Delete data source by UID"""
        return self.connection.instance.datasource.delete_datasource_by_uid(uid)

    def delete_by_name(self, name: str) -> dict:
        """Delete data source by name"""
        return self.connection.instance.datasource.delete_datasource_by_name(name)

    def get_all(self) -> list[dict]:
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