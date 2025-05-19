from typing import Optional
from pydantic import BaseModel, ConfigDict
from grafana_client import GrafanaApi


class NoCredsError(BaseException):
    ...


class GrafanaCreds(BaseModel):
    login: str
    password: str


class GrafanaConnection(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    instance: Optional[GrafanaApi] = None
    error: Optional[Exception] = None
