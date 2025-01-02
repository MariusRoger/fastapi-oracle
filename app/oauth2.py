from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app import app_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


settings = app_settings.get_settings()


def create_access_token(data: dict):

    expiration_time = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRATION_MINUTES
    )

    token = jwt.encode(
        data | {"exp": expiration_time},
        algorithm=settings.JWT_ALGORITHM,
        key=settings.JWT_SECRET_KEY,
    )

    return token


def get_current_username(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(
            token, algorithms=[settings.JWT_ALGORITHM], key=settings.JWT_SECRET_KEY
        )
        username: str = payload["username"]

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return username
