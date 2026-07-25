"""Shared response envelope used across the API for consistent error shape."""
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: dict | None = None
