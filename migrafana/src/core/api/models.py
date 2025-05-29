from typing import Optional
from pydantic import BaseModel, ConfigDict
from grafana_client import GrafanaApi


class NoGrafanaCredsError(Exception):
    ...


class GrafanaConnectionError(Exception):
    ...


class GrafanaCreds(BaseModel):
    login: Optional[str]
    password: Optional[str]
    token: Optional[str]


class GrafanaInstanceConfig(BaseModel):
    url: str
    credentials: GrafanaCreds
    master: bool


class GrafanaManagerConfig(BaseModel):
    instances: list[GrafanaInstanceConfig]


class GrafanaConnection(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    instance: Optional[GrafanaApi] = None
    error: Optional[Exception] = None
