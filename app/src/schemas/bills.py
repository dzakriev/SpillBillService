from pydantic import BaseModel, Field
from typing import List

class BillPosition(BaseModel):   
    name: str = Field(min_length=1, max_length=256)
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    total: float = Field(gt=0)

class ListPosition(BaseModel):
    pos_list: list[BillPosition]
