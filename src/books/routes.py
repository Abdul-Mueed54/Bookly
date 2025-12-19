from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from src.books.schemas import Book, UpdateBookModel
from src.books.books_data import books
from typing import List

book_routes = APIRouter()


@book_routes.get("/", response_model=List[Book])
async def get_all_books():
    return books


@book_routes.get("/{book_id}")
async def get_book_by_id(book_id: str):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")


@book_routes.post("/create-book")
async def craete_book(book_data: Book):
    for book in books:
        if book["id"] == book_data.id:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="book with this id alraedy exist",
            )
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book


@book_routes.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")


@book_routes.patch("/{book_id}")
async def update_book(book_id, updated_book_data: UpdateBookModel):
    for book in books:
        if book["id"] == book_id:
            book["title"] = updated_book_data.title
            book["author"] = updated_book_data.author
            book["publisher"] = updated_book_data.publisher
            book["published_year"] = updated_book_data.published_year
            book["language"] = updated_book_data.language
            book["pages"] = updated_book_data.pages
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")