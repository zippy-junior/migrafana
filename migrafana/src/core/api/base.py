from abc import ABC, abstractmethod
from typing import Self
from grafana_client import GrafanaApi

from core.api.models import (GrafanaConnection,
                             GrafanaConfig,
                             GrafanaConnectionError)
from core.journaling import internal_logger as i_logger


def connect(conf: GrafanaConfig):
    grafana_inst = GrafanaApi.from_url(
        url=conf.url,
        credential=(conf.creds.login, conf.creds.password)
    )
    try:
        grafana_inst.connect()
        return GrafanaConnection(instance=grafana_inst)
    except Exception as e:
        return GrafanaConnection(error=e)


class Manager(ABC):

    @classmethod
    @abstractmethod
    def from_config(cls, conf: GrafanaConfig) -> Self:
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

    def __init__(self, connection: GrafanaConnection):
        self.connection = connection

    @classmethod
    def from_config(cls, conf: GrafanaConfig) -> Self:
        connection: GrafanaConnection = connect(conf)
        if connection.error:
            i_logger.error(connection.error)
            raise GrafanaConnectionError(connection.error)
        else:
            return cls(connection)

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
