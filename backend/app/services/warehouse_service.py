from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cargo_item import CargoItem
from app.utils import error_codes


def scan_cargo_item(db: Session, qr_code: str, action: str) -> CargoItem:
    item = db.query(CargoItem).filter(CargoItem.qr_code == qr_code).first()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": error_codes.RESOURCE_NOT_FOUND, "message": "No cargo item matches this QR code."},
        )

    item.status = "in_warehouse" if action == "receive" else "dispatched"
    db.commit()
    db.refresh(item)
    return item
