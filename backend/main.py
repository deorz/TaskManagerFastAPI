from typing import Callable

from fastapi import FastAPI, Response, Request
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from backend.task_manager.database.base import create_session
from backend.task_manager.database.service import try_flush_commit

task_manager = FastAPI(
    title='TaskManagerFastAPI',
    description='Task Manager for Supercomputer',
    version='0.1',
)

task_manager.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def session_maker(request: Request, call_next: Callable) -> Response:
    """
    Middleware для добавления объекта сессии в объект
    запроса для дальнейшего использования.
    :param:         request - объект HTTP-запроса
    :param:         call_next - функция для передачи запроса в приложение
    """
    session = create_session()
    request.state.session = session
    try:
        response = await call_next(request)
    except SQLAlchemyError as ex:
        await request.state.session.rollback()
        return JSONResponse(
            content={
                'detail': ' '.join(arg for arg in ex.args)
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    await try_flush_commit(session=request.state.session, commit=True)
    await request.state.session.close()
    return response


task_manager.add_middleware(
    middleware_class=BaseHTTPMiddleware,
    dispatch=session_maker
)
