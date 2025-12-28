from pydantic import BaseModel, Field, EmailStr
from src.db.models import Book
import uuid
from src.reviews.schemas import ReviewModel
from datetime import datetime
from typing import List


class UserCreateModel(BaseModel):
    username: str = Field(max_length=20)
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel] = None


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str
