from pydantic import BaseModel

class ExampleDataCreate(BaseModel):
    name: str
    description: str = None
