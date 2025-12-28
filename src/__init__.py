from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.books.routes import book_routes
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from rich.console import Console
from src.errors import (
    create_exception_handler,
    InvalidCredentials,
    InvalidToken,
    UserAlreadyExist,
    UserNotFound,
    BookNotFound,
    ReevokedToken,
    RefreshTokenRequired,
    AccessTokenRequired,
    InsufficientPermission,
)

console = Console()


@asynccontextmanager
async def life_span(app: FastAPI):
    console.print("[bold white]server is starting ...[/bold white]")
    await init_db()
    yield
    console.print("[bold white]server has been stopped[/bold white]")


version = "v1"
app = FastAPI(
    title="Bookly",
    description="A REST API for book review web service",
    version=version,
)

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
        content={"message": "Oosp! Something went wrong", "error_code": "server_error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


app.include_router(book_routes, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/users", tags=["users"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
