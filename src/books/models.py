from sqlmodel import SQLModel, Column, Field
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: str
    author: str
    publisher: str
    published_year: int
    language: str
    pages: int
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default= datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default= datetime.now))
