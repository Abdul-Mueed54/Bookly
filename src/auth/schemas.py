from pydantic import BaseModel, Field, EmailStr
import uuid
from datetime import datetime


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


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str