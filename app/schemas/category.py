from pydantic import BaseModel
from typing import List

class CategoryCreate(BaseModel):
    name: str

class CategoryOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class CategoryAssign(BaseModel):
    category_ids: List[int]