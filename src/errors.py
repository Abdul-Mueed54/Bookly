from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status


class BooklyExceptions(Exception):
    """This is the base class for all Bookly errors"""

    pass


class InvalidToken(BooklyExceptions):
    """User has provided an invalid or expired token"""

    pass


class ReevokedToken(BooklyExceptions):
    """User has provided a token that has been revooked"""

    pass


class AccessTokenRequired(BooklyExceptions):
    """User has provided a refresh token when access token is required"""

    pass


class RefreshTokenRequired(BooklyExceptions):
    """User has provided a access token when refresh token is required"""

    pass


class UserAlreadyExist(BooklyExceptions):
    """User has provided an email that already has account"""

    pass


class InvalidCredentials(BooklyExceptions):
    """User has provide wrong email or password"""

    pass


class InsufficientPermission(BooklyExceptions):
    """User does not have the permission to perform an action"""

    pass


class BookNotFound(BooklyExceptions):
    """Book not found"""

    pass


class UserNotFound(BooklyExceptions):
    """User not found"""

    pass


def create_exception_handler(
    status_code: int, initial_details: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: Exception):
        return JSONResponse(content=initial_details, status_code=status_code)

    return exception_handler


def register_all_handlers(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExist,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_details={
                "message": "User with email already exists",
                "error": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_details={
                "message": "invalid email or password",
                "error": "invalid_credentials",
            },
        ),
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_details={
                "message": "User provided an invalid or expired token",
                "error": "invalid_token",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_details={
                "message": "User not found",
                "error": "User_not_found",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_details={
                "message": "book not found",
                "error": "Book_not_found",
            },
        ),
    )

    app.add_exception_handler(
        ReevokedToken,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_details={
                "message": "provided token has been revooked, please provide a new one",
                "error": "revooked_token",
            },
        ),
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            initial_details={
                "message": "User provided an access token, whereas refresh required",
                "error": "Refresh_token_required",
            },
        ),
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            initial_details={
                "message": "User provided a refresh token, whereas access required",
                "error": "Access_token_required",
            },
        ),
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_details={
                "message": "User does not have sufficient permissions to perform the task",
                "error": "Insufficient_permission",
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exception):

        return JSONResponse(
            content={
                "message": "Oosp! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
