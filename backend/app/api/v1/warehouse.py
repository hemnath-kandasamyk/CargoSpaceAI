import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.database.session import get_db
from app.models.user import User
from app.models.warehouse import Warehouse
from app.schemas.warehouse import InventoryScanRequest, InventoryScanResponse, WarehouseCapacityResponse
from app.services.warehouse_service import scan_cargo_item
from app.utils import error_codes
from fastapi import HTTPException, status

router = APIRouter(prefix="/warehouse", tags=["Warehouse"])


@router.post("/inventory/scan", response_model=InventoryScanResponse)
def scan_inventory(
    payload: InventoryScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("warehouse_staff", "admin")),
):
    item = scan_cargo_item(db, payload.qr_code, payload.action)
    return InventoryScanResponse(cargo_item_id=item.id, new_status=item.status)


@router.get("/{warehouse_id}/capacity", response_model=WarehouseCapacityResponse)
def get_warehouse_capacity(
    warehouse_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("warehouse_staff", "admin")),
):
    warehouse = db.get(Warehouse, warehouse_id)
    if warehouse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": error_codes.RESOURCE_NOT_FOUND, "message": "Warehouse not found."},
        )
    return warehouse
