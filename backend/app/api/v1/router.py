"""Aggregates every v1 sub-router into one, mounted under /api/v1 in main.py."""
from fastapi import APIRouter

from app.api.v1 import admin, ai, auth, driver, shipments, warehouse

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(shipments.router)
api_router.include_router(driver.router)
api_router.include_router(warehouse.router)
api_router.include_router(admin.router)
api_router.include_router(ai.router)
