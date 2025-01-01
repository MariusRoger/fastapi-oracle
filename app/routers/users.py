from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import database, database_models, pydantic_models, utils

router = APIRouter()


@router.get("")
async def get_users(db: Annotated[Session, Depends(database.get_db)]):
    users_retrieved: list[database_models.UsersTable] = db.query(
        database_models.UsersTable
    ).all()

    return users_retrieved


@router.post("")
async def create_user(
    db: Annotated[Session, Depends(database.get_db)], user: pydantic_models.UserToCreate
):
    new_user = database_models.UsersTable()
    new_user.hashed_password = utils.hash(user.password)  # TODO hash function
    new_user.username = user.username

    try:
        db.add(new_user)
        db.commit()
    except Exception as _:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not add new user",
        )

    return {"response": "User created."}
