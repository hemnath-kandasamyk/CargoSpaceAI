import uuid

from pydantic import BaseModel, Field


class InventoryScanRequest(BaseModel):
    qr_code: str
    action: str = Field(pattern="^(receive|dispatch)$")


class InventoryScanResponse(BaseModel):
    cargo_item_id: uuid.UUID
    new_status: str


class WarehouseCapacityResponse(BaseModel):
    warehouse_id: uuid.UUID
    name: str
    capacity_units: int
    current_load_units: int

    model_config = {"from_attributes": True}
