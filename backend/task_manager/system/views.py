from typing import List

from fastapi import APIRouter, status, Depends
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from backend.task_manager.database.models import System
from backend.task_manager.database.queries import get_entity, update_entity
from backend.task_manager.database.service import try_flush_commit
from backend.task_manager.system.schema import SystemOut, SystemIn, SystemBase
from backend.task_manager.utils.authentication import JWTBearer

system_router = APIRouter(prefix='/system')


@system_router.get('/', dependencies=[Depends(JWTBearer())], response_model=List[SystemOut])
async def get_systems(request: Request) -> List[SystemOut]:
    """Функция получения информации об активных системах"""
    systems: List[System] = await get_entity(
        session=request.state.session,
        model=System,
        order_by=(System.active.desc(), System.available_threads.desc())
    )
    return [SystemOut.from_orm(system) for system in systems]


@system_router.get('/{pk}', dependencies=[Depends(JWTBearer())], response_model=SystemOut)
async def get_system(request: Request, pk: int) -> SystemOut:
    """Функция получения информации о системе"""
    system: System = await get_entity(
        session=request.state.session,
        model=System,
        single=True,
        id_system=pk
    )
    return SystemOut.from_orm(system)


@system_router.post('/', dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
async def create_system(request: Request, system: SystemIn) -> None:
    """Функция создания записи о системе"""
    record: System = System(**system.dict(exclude_none=True))
    record.available_threads = record.threads
    request.state.session.add(record)
    await try_flush_commit(session=request.state.session, commit=False)


@system_router.patch('/{pk}', dependencies=[Depends(JWTBearer())], response_model=SystemOut)
async def update_system(request: Request, system: SystemBase,
                        pk: int) -> SystemOut:
    """Функция обновления записи о системе"""
    record: System = await get_entity(
        session=request.state.session,
        model=System,
        single=True,
        id_system=pk
    )
    if record.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя редактировать данные об активной системе'
        )
    updated_fields = system.dict(exclude_unset=True)
    update_entity(record=record, fields=updated_fields)
    await try_flush_commit(session=request.state.session, commit=False)
    return SystemOut.from_orm(record)


@system_router.post('/{pk}/state', dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
async def change_system_state(request: Request, pk: int):
    """Функция изменения состояния системы"""
    system: System = await get_entity(
        session=request.state.session,
        model=System,
        single=True,
        id_system=pk
    )
    system.active = not system.active
    await try_flush_commit(session=request.state.session, commit=False)
    return JSONResponse(
        content={
            'detail': 'Система успешно переведена в состояние {}'.format(
                'Активна' if system.active else 'Неактивна'
            )
        },
        status_code=status.HTTP_200_OK
    )


@system_router.delete('/{pk}', dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
async def delete_system(request: Request, pk: int) -> None:
    system: System = await get_entity(
        session=request.state.session,
        model=System,
        single=True,
        id_system=pk
    )
    if system.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя удалить активную систему'
        )
    await request.state.session.delete(system)
