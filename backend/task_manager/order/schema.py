from pydantic import BaseModel

from backend.task_manager.tasks.schema import TaskOut


class OrderOut(BaseModel):
    task: TaskOut
    order_number: int

    class Config:
        orm_mode = True
