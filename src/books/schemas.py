from pydantic import BaseModel
from datetime import datetime
import uuid


class Books(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_year: int
    language: str
    pages: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateBookModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_year: int
    language: str
    pages: int


class UpdateBookModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_year: int
    language: str
    pages: int
