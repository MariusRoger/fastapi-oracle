from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/")
async def get_root_params(query: str = None, limits: int = None):
    if query is not None or limits is not None:
        return {"response": f"query is {query} and limits is {limits}."}
    return {"response": "success !"}


@app.get("/{idx}")
async def get_path_variable(idx: int):
    return {"response": f"variable is {idx} !"}


@app.post("/")
async def get_request_body(item: Item):
    return item
