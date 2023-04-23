from uuid import uuid4
from typing import Optional

from pydantic import BaseModel, root_validator


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    username: Optional[str]


class UserIn(UserBase):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    guid: str = str(uuid4())


class UserOut(UserBase):
    id_user: int
    is_staff: bool
    first_name: str
    last_name: str
    email: str
    username: str

    class Config:
        orm_mode = True


class UpdateUserIn(UserBase):
    password: Optional[str]
    new_password: Optional[str]

    @root_validator
    def check_passwords(cls, values):
        password, new_password = (
            values.get('password'), values.get('password')
        )
        if not password and new_password:
            raise ValueError(
                'Для обновления пароля необходимо заполнить поля «Старый пароль» и «Новый пароль»'
            )

        return values
