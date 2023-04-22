from typing import Union, List, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from backend.task_manager.database.models import Base


async def get_entity(session: AsyncSession, model: Type[Base],
                     order_by: tuple = None, execute: bool = True,
                     single: bool = False, **filters
                     ) -> Union[Base, List[Base], Query]:
    """Функция получения сущности/списка сущностей из БД"""
    query = select(model)
    # Применение фильтров к запросу
    for key, value in filters.items():
        # Проверка наличия атрибута в сущности (модели)
        if hasattr(model, key):
            query = query.filter(
                getattr(model, key).in_(value)
                if isinstance(value, (list, tuple))
                else getattr(model, key).is_(value)
                if isinstance(value, bool)
                else getattr(model, key) == value
            )
    # Добавление сортировки к запросу
    if order_by:
        query = query.order_by(*order_by)
    # Если активен флаг execute, то выполняем запрос в БД
    if execute:
        result = await session.execute(query)
        return result.scalars().first() if single else result.scalars()

    return query


def update_entity(record: Base, fields: dict) -> Base:
    """Функция обновления записи по полям"""
    for key, value in fields.items():
        if hasattr(record, key):
            setattr(record, key, value)

    return record
