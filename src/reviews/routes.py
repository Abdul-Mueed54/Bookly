from fastapi import APIRouter, Depends
from src.reviews.schemas import ReviewCreateModel, ReviewModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.db.models import User
from src.reviews.service import ReviewService
from src.auth.dependencies import get_current_user

review_router = APIRouter()
review_service = ReviewService()


@review_router.post("/book/{book_uid}", response_model=ReviewModel)
async def add_review_to_book(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        book_uid=book_uid,
        review_data=review_data,
        session=session,
    )

    return new_review
