from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.get("/")
async def root():
    return {"message: Hello World"}

app.post("/items")
async def create_item(item: Item):
    return{"message": f"{item.name} is priced at ${item.price}"}