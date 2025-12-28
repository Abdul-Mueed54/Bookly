from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from src.reviews.schemas import ReviewModel
import uuid


class Books(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_year: int
    language: str
    pages: int
    user_uid: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookDetailModel(Books):
    reviews: List[ReviewModel] = []


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
