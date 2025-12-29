from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import time
from rich.console import Console
import logging

logger = logging.getLogger("uvicorn.access")
logger.disabled = True

console = Console()


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        processing_time = time.time() - start_time
        message = f"{request.client.host}:{request.client.port} - {request.method} - \
        {request.url.path} - {response.status_code} - completed after {processing_time}s"
        console.print(f"[bold white]{message}[/bold white]")
        return response

    @app.middleware("http")
    async def authorization(request: Request, call_next):
        if not "Authorization" in request.headers:
            return JSONResponse(
                content={
                    "message": "Not Authenticated",
                    "resolution": "Please provide the credentials to proceed",
                },
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        response = call_next(request)
        return response
