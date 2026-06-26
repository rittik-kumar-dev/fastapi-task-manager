# Data validation using Pydantic
from pydantic import BaseModel
from typing import List ,Any
class TakeSchema(BaseModel):
    id: int
    text: str
    completed: bool = False
    
class ResponseSchema(BaseModel):
        status:str
        data:list[Any]