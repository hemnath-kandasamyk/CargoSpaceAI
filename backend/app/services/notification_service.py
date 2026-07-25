import uuid

from sqlalchemy.orm import Session

from app.models.notification import Notification


def notify_user(db: Session, user_id: uuid.UUID, message: str, shipment_id: uuid.UUID | None = None) -> Notification:
    notification = Notification(user_id=user_id, message=message, shipment_id=shipment_id)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification
