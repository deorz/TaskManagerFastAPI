import asyncio
import base64
from uuid import uuid4

from sqlalchemy import select, func, ARRAY, String
from sqlalchemy.ext.asyncio import AsyncSession

from backend.task_manager.database.base import create_session
from backend.task_manager.database.models import File
from backend.task_manager.database.service import try_flush_commit
from backend.task_manager.settings import settings
from backend.task_manager.tasks.schema import FileIn


async def create_file_from_data(session: AsyncSession, data: FileIn):
    id_file = str(uuid4())
    file_dir = settings.BASE_DIR / settings.FILE_PATH
    file_dir.mkdir(exist_ok=True)
    file_path = file_dir / f'{id_file}.py'
    record = File(
        id_file=id_file,
        file_path=str(file_path),
        readable_file_name=data.name
    )
    file_content = data.body.split(',')[-1]

    with open(file_path, 'wb') as file:
        file.write(base64.b64decode(file_content))

    session.add(record)
    await try_flush_commit(session=session, commit=False)
    return record


async def delete_wrong_files():
    session: AsyncSession = create_session()
    files_dir = settings.BASE_DIR / settings.FILE_PATH

    if not files_dir.exists():
        files_dir.mkdir(exist_ok=True)
        await session.close()
        await asyncio.sleep(86400)

    task_files_query = select(
        func.array_agg(File.file_path, type_=ARRAY(String))
    )
    task_files = (await session.scalar(task_files_query)) or []
    for file in files_dir.iterdir():
        if str(file) not in task_files:
            file.unlink()

    await session.close()
    await asyncio.sleep(86400)
