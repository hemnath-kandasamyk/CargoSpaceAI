import uuid

from pydantic import BaseModel


class DeliveryStatusUpdateRequest(BaseModel):
    status: str  # e.g. out_for_delivery, delivered
    proof_image_url: str | None = None


class AssignedDeliveryResponse(BaseModel):
    id: uuid.UUID
    destination_address: str
    status: str

    model_config = {"from_attributes": True}
