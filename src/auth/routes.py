from fastapi import APIRouter, Depends, status
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel
from src.auth.service import UserService
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from fastapi.exceptions import HTTPException
from rich.console import Console
from datetime import timedelta
from fastapi.responses import JSONResponse
from src.auth.utils import create_access_token, decode_token, verify_password

console = Console()

auth_router = APIRouter()
user_service = UserService()
REFRESH_TOKEN_EXPIRY = 2


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    user = await user_service.user_exists(user_data.email, session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="user already exist"
        )

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)
    console.print(f"[bold green]{user}[/bold green]")

    if user:
        validate_password = verify_password(password, user.password)

        if validate_password:
            access_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)}
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "login successfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid email or password"
    )
