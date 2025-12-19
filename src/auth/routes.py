from fastapi import APIRouter, Depends, status
from src.auth.schemas import UserCreateModel
from src.auth.service import AuthService
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from fastapi.exceptions import HTTPException

auth_router = APIRouter()
auth_service = AuthService()


@auth_router.post("/signup")
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    user = auth_service.user_exists(user_data.email, session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user already exist"
        )

    new_user = auth_service.create_user(user_data, session)

    return new_user
