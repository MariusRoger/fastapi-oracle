from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import database, database_models, oauth2, pydantic_models

router = APIRouter()


@router.get("")
async def get_all_todos(
    db: Annotated[Session, Depends(database.get_db)],
    username: Annotated[str, Depends(oauth2.get_current_username)],
):

    todos_list: list[database_models.Todos] = (
        db.query(database_models.Todos)
        .filter(database_models.Todos.owner_username == username)
        .all()
    )

    return todos_list


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_todo(
    db: Annotated[Session, Depends(database.get_db)],
    todo: pydantic_models.Todo,
    username: Annotated[str, Depends(oauth2.get_current_username)],
):

    new_todo = database_models.Todos(owner_username=username, **todo.model_dump())

    try:
        db.add(new_todo)
        db.commit()
    except Exception as _:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not add new todo",
        )

    return {"response": "TODO added."}


@router.put("/{id}")
async def update_todo(
    db: Annotated[Session, Depends(database.get_db)],
    id: int,
    todo: pydantic_models.Todo,
    username: Annotated[str, Depends(oauth2.get_current_username)],
):

    todo_from_id_query = db.query(database_models.Todos).filter(
        database_models.Todos.id == id, database_models.Todos.owner_username == username
    )

    todo_from_id = todo_from_id_query.first()

    if todo_from_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO with id {id} does not exist.",
        )

    todo_from_id_query.update(todo.model_dump())
    db.commit()

    return todo_from_id_query.first()


@router.delete("/{id}")
async def delete_todo(
    db: Annotated[Session, Depends(database.get_db)],
    id: int,
    username: Annotated[str, Depends(oauth2.get_current_username)],
):

    todo_from_id_query = db.query(database_models.Todos).filter(
        database_models.Todos.id == id, database_models.Todos.owner_username == username
    )

    todo_from_id = todo_from_id_query.first()

    if todo_from_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO with id {id} does not exist.",
        )

    todo_from_id_query.delete()
    db.commit()

    return {"response": "TODO deleted."}
