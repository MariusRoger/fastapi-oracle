from datetime import datetime, timedelta, timezone

from jose import jwt

from app import app_settings

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
