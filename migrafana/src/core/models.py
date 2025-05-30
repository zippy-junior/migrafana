from typing import Literal, Optional
from pydantic import BaseModel, RootModel


class PatchOp(BaseModel):
    path: str
    op: Literal['test', 'add', 'remove', 'replace']
    value: Optional[int | bool | str | dict | list | tuple] = None


class Patch(RootModel):
    root: list[PatchOp]
