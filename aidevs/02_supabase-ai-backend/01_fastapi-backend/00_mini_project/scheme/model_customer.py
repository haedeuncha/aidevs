from typing import Any
from pydantic import BaseModel, Field

    
class Customer(BaseModel):
    id: str = Field(min_length=3, examples=["id01"])
    pwd: str= Field(min_length=4, examples=["pwd"])
    name: str= Field(min_length=5, examples=["Mr.Hong"])
    age: int= Field(ge=1, examples=[25])

class CustomerOut(BaseModel):
    id: str = Field(min_length=3, examples=["id01"])
    name: str= Field(min_length=5, examples=["Mr.Hong"])
    age: int= Field(ge=1, examples=[25])