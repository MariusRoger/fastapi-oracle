from fastapi import FastAPI

from app.routers import login, todos, users

app = FastAPI()
app.include_router(router=todos.router, tags=["Todos"], prefix="/todos")
app.include_router(router=users.router, tags=["Users"], prefix="/users")
app.include_router(router=login.router, tags=["Login"], prefix="/login")
