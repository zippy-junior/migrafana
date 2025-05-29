from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from grafana_client import GrafanaApi


class NoGrafanaInstanceCredentialsError(Exception):
    ...


class GrafanaConnectionError(Exception):
    ...


class GrafanaInstanceCredentials(BaseModel):
    username: Optional[str]
    password: Optional[str]
    token: Optional[str]


class GrafanaInstanceConfig(BaseModel):
    url: str
    credentials: GrafanaInstanceCredentials
    master: bool


class GrafanaManagerConfig(BaseModel):
    instances: list[GrafanaInstanceConfig]


class GrafanaManagerConnections(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    master: GrafanaApi
    slaves: Optional[List[GrafanaApi]]
