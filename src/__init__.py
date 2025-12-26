from fastapi import FastAPI
from src.books.routes import book_routes
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from rich.console import Console

console = Console()


@asynccontextmanager
async def life_span(app: FastAPI):
    console.print("[bold white]server is starting ...[/bold white]")
    await init_db()
    yield
    print("[bold white]server has been stopped[/bold white]")


version = "v1"
app = FastAPI(
    title="Bookly",
    description="A REST API for book review web service",
    version=version,
)
app.include_router(book_routes, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/users", tags=["users"])
