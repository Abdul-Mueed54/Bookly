from sqlalchemy.ext.asyncio.session import AsyncSession
from src.books.models import Book
from src.books.schemas import CreateBookModel, UpdateBookModel
from sqlmodel import select, desc
import uuid


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)

        return result

    async def get_book_by_uid(self, book_id: uuid, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_id)

        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None

    async def create_book(self, book_data: CreateBookModel, session: AsyncSession):
        created_book_data = book_data.model_dump()
        new_book = Book(**created_book_data)
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(
        self, book_id: uuid, updated_data: UpdateBookModel, session: AsyncSession
    ):
        book_to_update = self.get_book_by_uid(book_id, session)
        if book_to_update is not None:
            updated_book_data = updated_data.model_dump()

            for k, v in updated_book_data.items():
                setattr(book_to_update, k, v)
            await session.commit()

            return book_to_update
        return None

    async def delete_book(self, book_id, session: AsyncSession):
        book_to_delete = self.get_book_by_uid(book_id, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()

        else:
            return None

        pass
