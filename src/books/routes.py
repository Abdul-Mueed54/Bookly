from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import Books, UpdateBookModel, CreateBookModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from typing import List

book_routes = APIRouter()
book_service = BookService()


@book_routes.get("/", response_model=List[Books])
async def get_all_books(session: AsyncSession = Depends (get_session)):
    books = await book_service.get_all_books(session)
    return books


@book_routes.get("/{book_uid}", response_model=Books)
async def get_book_by_uid(book_uid: str, session: AsyncSession = Depends (get_session)):
    book = await book_service.get_book_by_uid(book_uid, session)
    if book is not None:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")


@book_routes.post("/create-book", response_model=Books, status_code=status.HTTP_201_CREATED)
async def craete_book(book_data: CreateBookModel, session: AsyncSession = Depends (get_session)):
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_routes.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends (get_session)):
    book = await book_service.delete_book(book_uid, session)
    if book is not None:
        return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")


@book_routes.patch("/{book_uid}", response_model=Books)
async def update_book(book_uid, updated_book_data: UpdateBookModel, session: AsyncSession = Depends (get_session)):
    book = await book_service.update_book(book_uid, updated_book_data, session)
    if book is not None:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")