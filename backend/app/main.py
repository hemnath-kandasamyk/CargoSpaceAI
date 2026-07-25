"""
Application entry point.
Run locally with: uvicorn app.main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config import settings
from app.middleware.error_handler import register_error_handlers

app = FastAPI(
    title="AI Cargo Tracking Platform API",
    version="1.0.0",
    description="Backend for shipment management, tracking, warehouse/fleet ops, and AI logistics analytics.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check():
    """Used by hosting platforms for uptime checks (see docs/deployment.md)."""
    return {"status": "ok"}
