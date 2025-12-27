from pydantic import BaseModel, Field, EmailStr
from src.books.models import Book
import uuid
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
    password: str
    email: EmailStr
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    books: List[Book]


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str