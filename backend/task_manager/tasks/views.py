from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import selectinload
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from backend.task_manager.database.models import Task, Order, User, File
from backend.task_manager.database.queries import get_entity, update_entity
from backend.task_manager.database.service import try_flush_commit
from backend.task_manager.status.enums import StatusEnum
from backend.task_manager.tasks.schema import (TaskOut, TaskIn, TaskBase, TaskResult, TaskOutShort)
from backend.task_manager.utils.authentication import JWTBearer, get_current_user
from backend.task_manager.utils.file_manage import create_file_from_data
from backend.task_manager.utils.order import reorder_queue

tasks_router = APIRouter(prefix='/tasks')


# ---------------------------- Базовый CDUD -----------------------------------

@tasks_router.get('/', dependencies=[Depends(JWTBearer())],
                  response_model=List[TaskOutShort])
async def get_tasks(
        request: Request, current_user: User = Depends(get_current_user)
) -> List[TaskOutShort]:
    """Функция для получения записей о тасках"""
    query = await get_entity(
        session=request.state.session,
        model=Task,
        order_by=(Task.priority.desc(),),
        execute=False,
        id_user=current_user.id_user
    )
    query = query.options(selectinload(Task.file), selectinload(Task.status))
    result = await request.state.session.execute(query)
    tasks: List[Task] = result.scalars()
    return [TaskOutShort.from_orm(task) for task in tasks]


@tasks_router.get('/{pk}', dependencies=[Depends(JWTBearer())],
                  response_model=TaskOut)
async def get_task(request: Request, pk: int) -> TaskOut:
    """Функция для получения одной записи о таске"""
    query = await get_entity(
        session=request.state.session,
        model=Task,
        single=True,
        id_task=pk,
        execute=False
    )
    query = query.options(selectinload(Task.file), selectinload(Task.status))
    result = await request.state.session.execute(query)
    task: Task = result.scalars().first()
    return TaskOut.from_orm(task)


@tasks_router.post('/', dependencies=[Depends(JWTBearer())],
                   status_code=status.HTTP_201_CREATED)
async def create_task(
        request: Request, task: TaskIn,
        current_user: User = Depends(get_current_user)
) -> None:
    """Функция для создания записи о таске"""
    file: File = await create_file_from_data(
        session=request.state.session,
        data=task.file,
        type=task.type
    )
    # Создание главной записи
    record: Task = Task(
        params=task.params,
        num_threads=task.num_threads,
        priority=task.priority,
        created_at=datetime.now().replace(microsecond=0),
        id_file=file.id_file,
        id_status=StatusEnum.created.value
    )
    record.id_user = current_user.id_user
    request.state.session.add(record)
    # Попытка вкатить в БД для получения ИД
    await try_flush_commit(session=request.state.session, commit=False)
    # Создание связанных сущностей
    request.state.session.add(Order(id_task=record.id_task))
    await try_flush_commit(session=request.state.session, commit=True)


@tasks_router.patch('/{pk}', dependencies=[Depends(JWTBearer())],
                    response_model=TaskOut)
async def update_task(request: Request, task: TaskBase, pk: int) -> TaskOut:
    """Функция для обновления записи о таске"""
    record: Task = await get_entity(
        session=request.state.session,
        model=Task,
        single=True,
        id_task=pk
    )
    if record.id_status != StatusEnum.created.value:
        raise HTTPException(
            detail=(
                'Задача не находится в статусе «Создана», изменение недоступно'
            ),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    updated_fields = task.dict(exclude_unset=True)
    update_entity(record=record, fields=updated_fields)
    await try_flush_commit(session=request.state.session, commit=False)
    return TaskOut.from_orm(record)


@tasks_router.delete('/{pk}', dependencies=[Depends(JWTBearer())],
                     status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(request: Request, pk: int) -> None:
    """Функция для обновления записи о таске"""
    query = await get_entity(
        session=request.state.session,
        model=Task,
        execute=False,
        id_task=pk
    )
    result = await request.state.session.execute(query)
    task: Task = result.scalars().first()
    if task.id_status in (StatusEnum.created.value, StatusEnum.exited.value):
        await request.state.session.delete(task)
        await try_flush_commit(session=request.state.session, commit=False)
        return None
    raise HTTPException(
        detail='Задача не находится в статусе «Создана», «Завершена», удаление недоступно',
        status_code=status.HTTP_400_BAD_REQUEST
    )


# ---------------------- Взаимодействие с тасками -----------------------------


@tasks_router.post('/{pk}/execute', dependencies=[Depends(JWTBearer())])
async def execute_task(request: Request, pk: int) -> JSONResponse:
    """Функция для отправки таски на исполнение"""
    query = await get_entity(
        session=request.state.session,
        model=Order,
        execute=False,
        id_task=pk
    )
    result = await request.state.session.execute(
        query.options(selectinload(Order.task).selectinload(Task.file))
    )
    order: Order = result.scalars().first()

    if order.task.id_status in (
            StatusEnum.scheduled, StatusEnum.running.value,
            StatusEnum.interrupted.value, StatusEnum.exited.value,
    ):
        raise HTTPException(
            detail=(
                'Задача уже была добавлена в очередь, '
                'повторный запуск недоступен'
            ),
            status_code=status.HTTP_400_BAD_REQUEST
        )

    order.order_number = 1
    order.task.id_status = StatusEnum.scheduled.value
    await try_flush_commit(session=request.state.session, commit=True)
    await reorder_queue(session=request.state.session)
    return JSONResponse(
        content={
            'detail': 'Задача успешно поставлена в очередь'
        },
        status_code=status.HTTP_200_OK
    )


@tasks_router.post('/{pk}/result', include_in_schema=False)
async def task_result(request: Request, task_result: TaskResult, pk: int):
    query = await get_entity(
        session=request.state.session,
        model=Order,
        execute=False,
        id_task=pk
    )
    result = await request.state.session.execute(
        query.options(selectinload(Order.task).selectinload(Task.system))
    )
    order: Order = result.scalars().first()

    order.task.output = task_result.output
    order.task.errors = task_result.errors
    order.task.exitcode = task_result.exitcode
    order.task.id_status = StatusEnum.exited.value
    order.task.system.available_threads += order.task.num_threads
    order.task.running_on = None
    order.order_number = None
    await try_flush_commit(session=request.state.session, commit=True)
    await reorder_queue(session=request.state.session)
