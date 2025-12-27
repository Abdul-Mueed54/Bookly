from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import Books, UpdateBookModel, CreateBookModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from typing import List
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_routes = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["user", "admin"]))


@book_routes.get("/", response_model=List[Books], dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    books = await book_service.get_all_books(session)
    return books

@book_routes.get("/user/{user_uid}", response_model=List[Books], dependencies=[role_checker])
async def get_user_books_submission(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    books = await book_service.get_user_books(user_uid, session)
    return books



@book_routes.get("/{book_uid}", response_model=Books, dependencies=[role_checker])
async def get_book_by_uid(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    book = await book_service.get_book_by_uid(book_uid, session)
    if book is not None:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")


@book_routes.post(
    "/create-book",
    response_model=Books,
    status_code=status.HTTP_201_CREATED,
    dependencies=[role_checker],
)
async def craete_book(
    book_data: CreateBookModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    user_uid = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(book_data, user_uid, session)
    return new_book


@book_routes.delete(
    "/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    book = await book_service.delete_book(book_uid, session)
    if book is not None:
        return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")


@book_routes.patch("/{book_uid}", response_model=Books, dependencies=[role_checker])
async def update_book(
    book_uid,
    updated_book_data: UpdateBookModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    book = await book_service.update_book(book_uid, updated_book_data, session)
    if book is not None:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")
