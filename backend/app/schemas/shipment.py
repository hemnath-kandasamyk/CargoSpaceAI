import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ShipmentCreateRequest(BaseModel):
    destination_address: str = Field(min_length=1)
    weight_kg: float = Field(gt=0)
    declared_value: float | None = Field(default=None, ge=0)
    origin_warehouse_id: uuid.UUID | None = None


class ShipmentResponse(BaseModel):
    id: uuid.UUID
    customer_id: uuid.UUID
    driver_id: uuid.UUID | None
    status: str
    weight_kg: float
    declared_value: float | None
    destination_address: str
    estimated_delivery: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TrackingHistoryEntry(BaseModel):
    status: str
    location: str | None
    updated_at: datetime

    model_config = {"from_attributes": True}


class ShipmentTrackingResponse(BaseModel):
    shipment: ShipmentResponse
    history: list[TrackingHistoryEntry]


class PaginatedShipments(BaseModel):
    items: list[ShipmentResponse]
    page: int
    page_size: int
    total: int
