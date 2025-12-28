from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse


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
