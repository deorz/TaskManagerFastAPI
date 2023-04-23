from time import time

from fastapi import Request, HTTPException, Depends
from fastapi.security import (HTTPBearer, HTTPAuthorizationCredentials,
                              OAuth2PasswordBearer)
from jose import jwt, JWTError
from starlette import status

from backend.task_manager.database.base import create_session
from backend.task_manager.database.models import User
from backend.task_manager.database.queries import get_entity
from backend.task_manager.settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(jwtoken=credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code."
            )

    def verify_jwt(self, jwtoken: str) -> bool:
        is_valid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except JWTError:
            payload = None
        if payload:
            is_valid = True

        return is_valid


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return (
            decoded_token if decoded_token["expires"] >= time() else None
        )
    except JWTError:
        return {}


def signJWT(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "expires": time() + settings.EXPIRE
    }
    token = jwt.encode(
        claims=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(
        token=token,
        key=settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    session = create_session()
    email: str = payload.get("user_id")
    user: User = await get_entity(
        session=session,
        model=User,
        single=True,
        execute=True,
        email=email
    )

    if not user:
        raise HTTPException(
            detail='Неверный токен авторизации',
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    await session.close()
    return user
