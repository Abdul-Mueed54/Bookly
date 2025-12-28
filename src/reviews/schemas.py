from pydantic import BaseModel
import uuid
from typing import Optional
from datetime import datetime


class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int
    review_text: str
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime


class ReviewCreateModel(BaseModel):
    rating: int
    review_text: str
