from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request

from backend.task_manager.database.models import User
from backend.task_manager.database.queries import get_entity, update_entity
from backend.task_manager.database.service import try_flush_commit
from backend.task_manager.users.schema import UserOut, UserIn, UpdateUserIn
from backend.task_manager.utils.authentication import JWTBearer, get_current_user
from backend.task_manager.utils.hasher import Hasher

users_router = APIRouter(prefix='/users')


@users_router.get('/', dependencies=[Depends(JWTBearer())], response_model=List[UserOut])
async def get_users(request: Request) -> List[UserOut]:
    """Функция получения списка пользователей"""
    records = await get_entity(
        session=request.state.session,
        model=User,
    )
    return [UserOut.from_orm(record) for record in records]


@users_router.get('/me', dependencies=[Depends(JWTBearer())], response_model=UserOut)
async def get_user(current_user: User = Depends(get_current_user)) -> UserOut:
    """Функция получения одного пользователя"""
    return UserOut.from_orm(current_user)


@users_router.get('/{pk}', dependencies=[Depends(JWTBearer())], response_model=UserOut)
async def get_user(request: Request, pk: int) -> UserOut:
    """Функция получения одного пользователя"""
    record = await get_entity(
        session=request.state.session,
        model=User,
        single=True,
        id_user=pk
    )
    return UserOut.from_orm(record)


@users_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(request: Request, user: UserIn) -> None:
    """Функция создания записи о пользователе"""
    record = User(**user.dict())
    record.password = Hasher.hash_password(password=user.password)
    request.state.session.add(record)
    await try_flush_commit(session=request.state.session, commit=True)


@users_router.patch('/{pk}', dependencies=[Depends(JWTBearer())], response_model=UserOut)
async def update_user(
        request: Request, user: UpdateUserIn, pk: int,
        current_user: User = Depends(get_current_user)
) -> UserOut:
    """Функция обновления записи о пользователе"""
    record = await get_entity(
        session=request.state.session,
        model=User,
        single=True,
        id_user=pk
    )
    if current_user.guid != record.guid:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
        )
    updated_fields = user.dict(exclude_unset=True)
    if 'password' in updated_fields.keys() or 'new_password' in updated_fields.keys():
        Hasher.check_password(
            plain_password=updated_fields['password'],
            hashed_password=record.password
        )
        updated_fields['password'] = Hasher.hash_password(
            password=updated_fields['new_password']
        )
    update_entity(record=record, fields=updated_fields)
    await try_flush_commit(session=request.state.session, commit=False)
    return UserOut.from_orm(record)


@users_router.delete('/{pk}', dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        request: Request, pk: int,
        current_user: User = Depends(get_current_user)
) -> None:
    """Функция удаления записи о пользователе"""
    record = await get_entity(
        session=request.state.session,
        model=User,
        single=True,
        id_user=pk
    )
    if current_user.guid != record.guid:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
        )
    request.state.session.delete(record)
    await try_flush_commit(session=request.state.session, commit=True)
