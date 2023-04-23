from typing import Optional

from pydantic import BaseModel


class SystemBase(BaseModel):
    threads: Optional[int]
    active: Optional[bool]
    host: Optional[str]


class SystemOut(SystemBase):
    id_system: int
    threads = int
    available_threads: int
    active: bool

    class Config:
        orm_mode = True


class SystemIn(SystemBase):
    threads: int
    active: bool = False
