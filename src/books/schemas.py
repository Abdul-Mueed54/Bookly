from pydantic import BaseModel
from datetime import datetime

class Books(BaseModel):
    id: str
    title: str
    author: str
    publisher: str
    published_year: int
    language: str
    pages: int
    created_at: datetime
    update_at: datetime

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