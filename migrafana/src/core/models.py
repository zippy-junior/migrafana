from typing import Optional
from pydantic import BaseModel, Field


class NoCredsError(BaseException):
    ...


class GrafanaConfig(BaseModel):
    url: str
    username: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None


class PatchConfig(BaseModel):
    path: str
    operations: list[dict] = Field(default_factory=list)
