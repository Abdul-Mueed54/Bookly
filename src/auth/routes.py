from fastapi import APIRouter, Depends, status
from src.auth.schemas import UserCreateModel, UserModel
from src.auth.service import UserService
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from fastapi.exceptions import HTTPException
from rich.console import Console

console = Console()

auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/signup", response_model= UserModel, status_code= status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    user = await user_service.user_exists(user_data.email, session) 
    console.print (f"[bold green]{user}[/bold green]")
    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user already exist"
        )

    new_user = await user_service.create_user(user_data, session)

    return new_user
