from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def try_flush_commit(
        session: AsyncSession, commit: bool = False
) -> None:
    """Метод для попытки вкатить изменения в БД"""
    try:
        await session.flush()
    except IntegrityError as ex:
        await session.rollback()
        raise ex
    else:
        if commit:
            await session.commit()
