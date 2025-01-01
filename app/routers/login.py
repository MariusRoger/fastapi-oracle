from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import database, database_models, utils

router = APIRouter()


# OAuth2
@router.post("")
async def login(
    db: Annotated[Session, Depends(database.get_db)],
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = (
        db.query(database_models.UsersTable)
        .filter(database_models.UsersTable.username == user_credentials.username)
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

    # generate the access token

    return {"access_token": "token here", "token_type": "bearer"}
