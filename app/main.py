from fastapi import FastAPI

from app import database

app = FastAPI()


@app.get("/")
async def get_root_with_db():
    return {"response": "Hello World !"}
