from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import contains_eager, selectinload
from starlette.requests import Request

from backend.task_manager.database.models import Order, User, Task
from backend.task_manager.database.queries import get_entity
from backend.task_manager.order.schema import OrderOut
from backend.task_manager.utils.authentication import JWTBearer, get_current_user

order_router = APIRouter(prefix='/order')


@order_router.get('/', dependencies=[Depends(JWTBearer())], response_model=List[OrderOut])
async def get_orders(
        request: Request, current_user: User = Depends(get_current_user)
) -> List[OrderOut]:
    """Функция получения очереди исполнения"""
    query = await get_entity(
        session=request.state.session,
        model=Order,
        order_by=(Order.order_number.asc(),),
        single=False,
        execute=False,
    )
    query = query.join(
        Task, Task.id_task == Order.id_task
    ).options(
        contains_eager(Order.task).options(
            selectinload(Task.file),
            selectinload(Task.status)
        )
    ).filter(
        Task.id_user == current_user.id_user,
        Order.order_number.isnot(None)
    )
    result = await request.state.session.execute(query)
    order: List[Order] = result.scalars()
    return [OrderOut.from_orm(record) for record in order]
