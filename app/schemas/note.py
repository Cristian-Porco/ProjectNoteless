from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class NoteVersionSchema(BaseModel):
    id: int
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True

class NoteCreate(BaseModel):
    title: str
    content: str
    is_public: bool = False
    category_ids: List[int] = []

class NoteOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    is_public: bool
    audio_file: Optional[str]
    versions: List[NoteVersionSchema]

    class Config:
        orm_mode = True