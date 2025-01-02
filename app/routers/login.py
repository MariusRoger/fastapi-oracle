from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import database, database_models, oauth2, utils

router = APIRouter()


# OAuth2
@router.post("")
async def login(
    db: Annotated[Session, Depends(database.get_db)],
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = (
        db.query(database_models.Users)
        .filter(database_models.Users.username == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    if not utils.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    access_token = oauth2.create_access_token({"username": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
