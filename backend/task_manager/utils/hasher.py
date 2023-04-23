from passlib.context import CryptContext

pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def check_password(plain_password: str, hashed_password: str) -> None:
        if not pswd_context.verify(plain_password, hashed_password):
            raise ValueError('Неверный пароль')

    @staticmethod
    def hash_password(password: str) -> str:
        return pswd_context.hash(password)
