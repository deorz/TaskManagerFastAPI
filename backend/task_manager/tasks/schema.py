from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel

from backend.task_manager.status.schema import StatusOut


class TaskBase(BaseModel):
    params: Optional[str]
    num_threads: Optional[int]
    priority: Optional[int]


class FileOut(BaseModel):
    readable_file_name: str

    class Config:
        orm_mode = True


class TaskOutShort(TaskBase):
    id_task: int
    params: Optional[str]
    num_threads: int
    priority: int
    created_at: datetime
    file: Optional[FileOut]
    status: Optional[StatusOut]

    class Config:
        orm_mode = True


class TaskOut(TaskBase):
    id_task: int
    params: Optional[str]
    num_threads: int
    priority: int
    created_at: datetime
    file: Optional[FileOut]
    output: Optional[str]
    errors: Optional[str]
    exitcode: Optional[int]
    status: Optional[StatusOut]

    class Config:
        orm_mode = True


class FileIn(BaseModel):
    name: str
    mimetype: str
    body: str


class TaskIn(TaskBase):
    file: FileIn
    params: Union[str, None] = None
    num_threads: int
    priority: int
    created_at: datetime = datetime.now().replace(microsecond=0)


class TaskResult(BaseModel):
    process_id: int
    output: str
    errors: str
    exitcode: int
