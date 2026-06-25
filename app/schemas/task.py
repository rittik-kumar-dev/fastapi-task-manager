# Data validation using Pydantic
from pydantic import BaseModel
class TakeSchema(BaseModel):
    id: int
    text: str
    completed: bool = False