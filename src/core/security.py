from datetime import datetime, timedelta
from typing import Optional

import jwt
import bcrypt
import secrets
from bson import ObjectId
from pydantic import ValidationError

from src import schemas
from src.core import settings


def create_access_token(
        user_id: str | ObjectId,
        expire_time: timedelta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
) -> str:
    expires = datetime.utcnow() + expire_time
    payload = schemas.TokenPayload(
        user_id=str(user_id),
        expires=expires.timestamp()
    )
    return jwt.encode(
        payload.dict(),
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


def get_user_id_from_access_token(token: str) -> Optional[str]:
    try:
        payload = schemas.TokenPayload(**jwt.decode(
            token,
            key=settings.JWT_SECRET,
            algorithms=settings.JWT_ALGORITHM
        ))
    except (jwt.DecodeError, ValidationError):
        return None
    return payload.user_id


def get_hashed_password(password: str) -> str:
    return str(
        bcrypt.hashpw(
            bytes(password, encoding='utf8'),
            salt=bcrypt.gensalt()
        ),
        encoding='utf8'
    )


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        bytes(password, encoding='utf8'),
        bytes(hashed_password, encoding='utf8')
    )


def get_webhook_key():
    return secrets.token_urlsafe()
