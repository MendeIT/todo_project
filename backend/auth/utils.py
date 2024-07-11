import datetime

import bcrypt
import jwt
from fastapi import HTTPException, status

from api.schemas.users import UserLoginSchemas
from core.config import settings

TIME_NOW = datetime.datetime.now(datetime.UTC)


def create_jwt_token(user: UserLoginSchemas, user_id: int) -> str:
    """Функция encode/кодирования для создания JWT токена."""

    payload = user.model_dump()
    expiration_time = TIME_NOW + datetime.timedelta(
        minutes=settings.TOKEN_EXPIRATION_DATE_IN_MINUTES
    )

    payload.update({
        'iat': TIME_NOW,
        'exp': expiration_time,
        'user_id': user_id,
    })

    token = jwt.encode(
        payload=payload,
        key=settings.JWT_PRIVATE_PATH.read_text(),
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def read_jwt_token(token: str) -> str:
    """Функция decode/декодирования User'а по токену."""

    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.JWT_PUBLIC_PATH.read_text(),
            algorithms=[settings.JWT_ALGORITHM]
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            detail='Access Token has expired or expiration date is invalid!',
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            detail='Invalid Token',
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"}
        )
    else:
        return payload


def hashed_password(password: str) -> bytes:
    """Метод хэширования пароля с добавлением 'соли'."""

    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()

    return bcrypt.hashpw(pwd_bytes, salt).decode()


def vaidate_password(password: str, hashed_password: bytes) -> bool:
    """Метод сопаставления паролей."""
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
