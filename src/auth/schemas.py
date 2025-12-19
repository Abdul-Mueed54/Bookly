from pydantic import BaseModel, Field, EmailStr


class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: EmailStr
    password: str = Field(min_length=6)
