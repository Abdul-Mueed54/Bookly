from fastapi import APIRouter, Depends, status
from src.auth.schemas import (
    UserCreateModel,
    UserModel,
    UserLoginModel,
    UserBooksModel,
    EmailModel,
    PasswordResetRequestModel,
    PasswordResetConfirmModel,
)
from src.auth.service import UserService
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from fastapi.exceptions import HTTPException
from rich.console import Console
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from src.config import Config
from src.auth.utils import (
    create_access_token,
    verify_password,
    generate_passwd_hash,
    create_url_safe_token,
    decode_url_safe_token,
)
from src.auth.dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from src.db.redis import add_jti_to_blocklist
from src.mail import create_message, mail
from src.errors import UserAlreadyExist, InvalidCredentials, InvalidToken, UserNotFound

console = Console()

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])
REFRESH_TOKEN_EXPIRY = 2


@auth_router.post("/send_mail")
async def send_mail(emails: EmailModel):
    emails = emails.addresses

    html = "<h1>Welcome to the App</h1>"

    message = create_message(recipients=emails, subject="Welcome Message", body=html)

    await mail.send_message(message)

    return {"message": f"mail has been sent to {emails}"}


@auth_router.post(
    "/signup",
    # response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    user = await user_service.user_exists(user_data.email, session)
    if user:
        raise UserAlreadyExist()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": user_data.email})
    link = f"http://{Config.DOMAIN}/api/v1/users/verify/{token}"

    html_message = f"""
        <h1>Verify your Email</h1>
        <p>Please click this <a href="{link}">link</a> to verify your Email
    """
    message = create_message(
        recipients=[user_data.email], subject="Verify Your Email", body=html_message
    )

    await mail.send_message(message)

    return {
        "message": "Your Account has been created successfully, check your email to verify account",
        "user": new_user,
    }


@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True}, session)
        return JSONResponse(
            content={"message": "Account Verified Successfully"},
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content={"message": "Error Occured during Verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


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

    raise InvalidCredentials()


@auth_router.get("/refresh-token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details.get("exp")

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()


@auth_router.get("/me", response_model=UserBooksModel)
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


"""
1. PROVIDE THE EMAIL -> password reset request
2. SEND PASSWORD RESET LINK
3. RESET PASSWORD -> password reset confirm
"""


@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestModel):
    token = create_url_safe_token({"email": email_data.email})
    link = f"http://{Config.DOMAIN}/api/v1/users/password-reset-confirm/{token}"

    html_message = f"""
        <h1>Verify your Email</h1>
        <p>Please click this <a href="{link}">link</a> to Reset your password
    """
    message = create_message(
        recipients=[email_data.email], subject="Reset your password", body=html_message
    )

    await mail.send_message(message)

    return JSONResponse(
        content={
            "message": "Please check your email for instructions to reset your password",
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.get("/password-reset-confirm/{token}")
async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):
    if passwords.new_password != passwords.confirm_new_password:
        raise HTTPException(
            detail="passwords do not match", status_code=status.HTTP_400_BAD_REQUEST
        )
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        passwd_hash = generate_passwd_hash(passwords.new_password)
        await user_service.update_user(user, {"password": passwd_hash}, session)
        return JSONResponse(
            content={"message": "Password updated Successfully"},
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content={"message": "Error Occured during resetting"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
