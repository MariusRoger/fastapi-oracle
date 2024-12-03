from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app import database, database_models, pydantic_models

app = FastAPI()


@app.get("/todos")
async def get_all_todos(db: Annotated[Session, Depends(database.get_db)]):

    todos_list: list[database_models.TodosTable] = db.query(
        database_models.TodosTable
    ).all()

    return todos_list


@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(
    db: Annotated[Session, Depends(database.get_db)], todo: pydantic_models.Todo
):

    new_todo = database_models.TodosTable(**todo.model_dump())

    try:
        db.add(new_todo)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not add new todo",
        )

    return {"response": "TODO added."}


@app.delete("/todos/{id}")
async def delete_todo(db: Annotated[Session, Depends(database.get_db)], id: int):

    todo_from_id_query = db.query(database_models.TodosTable).filter(
        database_models.TodosTable.id == id
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


@app.put("/todos/{id}")
async def update_todo(
    db: Annotated[Session, Depends(database.get_db)],
    id: int,
    todo: pydantic_models.Todo,
):

    todo_from_id_query = db.query(database_models.TodosTable).filter(
        database_models.TodosTable.id == id
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
