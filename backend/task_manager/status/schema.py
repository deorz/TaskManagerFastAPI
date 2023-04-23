from pydantic import BaseModel


class StatusOut(BaseModel):
    id_status: int
    name: str

    class Config:
        orm_mode = True
