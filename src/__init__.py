from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.books.routes import book_routes
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from rich.console import Console
from src.errors import register_all_handlers
from src.middleware import register_middleware

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
    contact={
        "email": "mueed9972@gmail.com"
    }
)

register_all_handlers(app)
register_middleware(app)


app.include_router(book_routes, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/users", tags=["users"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
