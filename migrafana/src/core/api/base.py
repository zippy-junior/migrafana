from abc import ABC, abstractmethod
from typing import Self
from grafana_client import GrafanaApi

from core.api.models import (GrafanaInstanceConfig,
                             GrafanaManagerConfig,
                             GrafanaConnectionError,
                             GrafanaManagerConnections)
from core.journaling import internal_logger as i_logger


class Manager(ABC):

    @classmethod
    @abstractmethod
    def from_config(cls, conf: GrafanaManagerConfig) -> Self:
        ...

    @abstractmethod 
    def get_by_uid(self, uid: str) -> dict:
        ...

    @abstractmethod
    def create(self, instance: dict) -> dict:
        ...

    @abstractmethod
    def update(self, instance: dict) -> dict:
        ...

    @abstractmethod
    def delete(self, uid: str) -> dict:
        ...

    @abstractmethod
    def search(self, query: str = "", tag: str = "") -> dict:
        ...


class GrafanaBaseManager():

    def __init__(self, connections: GrafanaManagerConnections):
        self.connections = connections

    @classmethod
    def from_config(cls, conf: GrafanaManagerConfig) -> Self:
        master = None
        slaves = []
        for instance in conf.instances:
            connection: GrafanaApi = cls.connect_to_instance(instance)
            if instance.master:
                master = connection
            else:
                slaves.append(connection)
        connections = {
            'master': master,
            'slaves': slaves if len(slaves) > 0 else None
        }
        return cls(GrafanaManagerConnections(**connections))

    def connect_to_instance(inst_conf: GrafanaInstanceConfig) -> GrafanaApi:
        instance = GrafanaApi.from_url(
            url=inst_conf.url,
            credential=inst_conf.credentials.token or (inst_conf.credentials.username,
                                                       inst_conf.credentials.password)
        )
        try:
            instance.connect()
            return instance
        except Exception as e:
            i_logger.error(e)
            raise GrafanaConnectionError(f"Can't connect to Grafana instance {inst_conf.url}: {e}")

    def get_by_uid(self, uid: str) -> dict:
        raise NotImplementedError()

    def create(self, instance: dict) -> dict:
        raise NotImplementedError()

    def update(self, instance: dict) -> dict:
        raise NotImplementedError()

    def delete(self, uid: str) -> dict:
        raise NotImplementedError()

    def search(self, query: str = "", tag: str = "") -> dict:
        raise NotImplementedError()
