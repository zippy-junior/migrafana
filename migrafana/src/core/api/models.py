from typing import Optional
from pydantic import BaseModel, ConfigDict
from grafana_client import GrafanaApi


class NoCredsError(Exception):
    ...


class GrafanaConnectionError(Exception):
    ...


class Creds(BaseModel):
    login: Optional[str]
    password: Optional[str]
    token: Optional[str]


class GrafanaConfig(BaseModel):
    url: str
    creds: Creds


class GrafanaConnection(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    instance: Optional[GrafanaApi] = None
    error: Optional[Exception] = None
