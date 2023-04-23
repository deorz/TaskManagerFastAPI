from fastapi import Depends, Request, APIRouter
from starlette import status
from starlette.exceptions import HTTPException

from backend.task_manager.auth.schema import AuthUser
from backend.task_manager.database.models import User
from backend.task_manager.database.queries import get_entity
from backend.task_manager.utils.authentication import signJWT
from backend.task_manager.utils.hasher import Hasher

auth_router = APIRouter(prefix='/auth')


@auth_router.post('/token')
async def auth(request: Request, request_user: AuthUser):
    """Метод для аутентификации пользователя"""
    user = await get_entity(
        session=request.state.session,
        model=User,
        single=True,
        execute=True,
        email=request_user.email
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль"
        )

    Hasher.check_password(
        plain_password=request_user.password,
        hashed_password=user.password
    )

    access_token = signJWT(user.email)

    return {
        'access_token': access_token,
    }
