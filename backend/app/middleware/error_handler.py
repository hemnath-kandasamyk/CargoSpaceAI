"""
Global exception handlers so every error response follows the same
{ error_code, message, details } shape described in docs/api-reference.md,
instead of FastAPI's default {"detail": ...} for unhandled cases.
"""
import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.utils import error_codes

logger = logging.getLogger("app")


def register_error_handlers(app: FastAPI) -> None:

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        # Routes/services already raise HTTPException with a structured `detail`
        # dict — pass it through as-is if it's already in the expected shape.
        if isinstance(exc.detail, dict) and "error_code" in exc.detail:
            body = exc.detail
        else:
            body = {"error_code": "HTTP_ERROR", "message": str(exc.detail), "details": None}
        return JSONResponse(status_code=exc.status_code, content=body)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error_code": error_codes.VALIDATION_ERROR,
                "message": "Request validation failed.",
                "details": {"errors": exc.errors()},
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception on %s %s", request.method, request.url)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred.",
                "details": None,
            },
        )
