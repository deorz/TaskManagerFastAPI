import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.task_manager.database.base import create_session
from backend.task_manager.database.models import Task, Order, System
from backend.task_manager.database.service import try_flush_commit
from backend.task_manager.status.enums import StatusEnum
from backend.task_manager.utils.process_manage import run_process


async def run_tasks_loop():
    while True:
        session: AsyncSession = create_session()

        tasks_query = await session.execute(
            select(Task).join(
                Order, Order.id_task == Task.id_task
            ).options(
                selectinload(Task.file)
            ).order_by(
                Order.order_number.asc()
            ).filter(
                Order.order_number.isnot(None),
                Task.running_on.is_(None),
                Task.id_status == StatusEnum.scheduled.value
            )
        )

        tasks = tasks_query.scalars().all()

        if tasks:
            systems_query = await session.execute(
                select(System).filter(
                    System.active.is_(True),
                    System.available_threads > 0
                ).order_by(
                    System.available_threads.asc()
                )
            )

            systems = systems_query.scalars().all()

            for task in tasks:
                system_to_run = None
                for system in systems:
                    if system.available_threads >= task.num_threads:
                        system_to_run = system
                        break

                if not system_to_run:
                    continue

                system_to_run.available_threads -= task.num_threads
                task.running_on = system_to_run.id_system
                task.id_status = StatusEnum.running.value

                await try_flush_commit(session=session, commit=False)

                run_process(task=task, file=task.file, system=system_to_run, id_task=task.id_task)
                await try_flush_commit(session=session, commit=True)

        await session.close()
        await asyncio.sleep(20)
