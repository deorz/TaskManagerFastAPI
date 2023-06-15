from typing import Callable

from fastapi import FastAPI, Response, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from backend.task_manager.auth.views import auth_router
from backend.task_manager.database.base import create_session, engine
from backend.task_manager.database.service import try_flush_commit
from backend.task_manager.order.views import order_router
from backend.task_manager.system.views import system_router
from backend.task_manager.tasks.views import tasks_router
from backend.task_manager.users.views import users_router
from backend.task_manager.utils.file_manage import delete_wrong_files
from backend.task_manager.utils.tasks_loop import run_tasks_loop

task_manager = FastAPI(
    title='TaskManagerFastAPI',
    description='Task Manager for Supercomputer',
    version='0.1',
    debug=True
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


@task_manager.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body
        },
    )


@task_manager.on_event("startup")
async def startup():
    import asyncio
    asyncio.create_task(run_tasks_loop())
    asyncio.create_task(delete_wrong_files())


@task_manager.on_event("shutdown")
async def shutdown():
    await engine.dispose()


task_manager.include_router(router=users_router, prefix='/v1')
task_manager.include_router(router=tasks_router, prefix='/v1')
task_manager.include_router(router=order_router, prefix='/v1')
task_manager.include_router(router=system_router, prefix='/v1')
task_manager.include_router(router=auth_router, prefix='/v1')
