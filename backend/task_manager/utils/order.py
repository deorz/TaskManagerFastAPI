from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import select

from backend.task_manager.database.models import Order, Task
from backend.task_manager.database.service import try_flush_commit


async def reorder_queue(session: AsyncSession) -> None:
    order_query = await session.execute(
        select(Order).join(Task, Task.id_task == Order.id_task).options(
            contains_eager(Order.task)
        ).order_by(
            Task.priority.desc(), Task.created_at.asc(),
        ).filter(
            Order.order_number.isnot(None)
        )
    )
    orders = order_query.scalars().all()
    for (order, value) in zip(orders, list(range(1, len(orders) + 1))):
        order.order_number = value
    await try_flush_commit(session=session, commit=False)
