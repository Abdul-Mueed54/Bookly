from fastapi import APIRouter, Depends, status
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel
from src.auth.service import UserService
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from fastapi.exceptions import HTTPException
from rich.console import Console
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from src.auth.utils import create_access_token, verify_password
from src.auth.dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from src.db.redis import add_jti_to_blocklist

console = Console()

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])
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

    if user:
        validate_password = verify_password(password, user.password)

        if validate_password:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "user_role": user.role,
                }
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


@auth_router.get("/refresh-token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details.get("exp")

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or Expire Token"
    )


@auth_router.get("/me")
async def ge_current_user(
    user=Depends(get_current_user), role: bool = Depends(role_checker)
):
    return user


@auth_router.get("/logout")
async def revooke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "logged out successfully"}, status_code=status.HTTP_200_OK
    )
