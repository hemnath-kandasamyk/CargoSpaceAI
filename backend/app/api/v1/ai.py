"""
Thin routing layer over the ML inference module (see /ml/inference in the
project root — not part of this backend package). The backend NEVER trains
models at request time; it only loads a cached joblib artifact and predicts.

NOTE: `run_inference` below is a placeholder until /ml/inference is wired in.
Replace `_placeholder_predict` with a real import once model artifacts exist,
e.g.: `from ml.inference.delay_model import predict_delay`
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.database.session import get_db
from app.models.user import User
from app.services.shipment_service import get_shipment_or_404
from app.utils import error_codes

router = APIRouter(prefix="/ai", tags=["AI Prediction"])


def _placeholder_predict(kind: str) -> dict:
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail={
            "error_code": error_codes.MODEL_UNAVAILABLE,
            "message": f"No trained model available yet for '{kind}'. See ml/training/.",
        },
    )


@router.get("/predict/delay/{shipment_id}")
def predict_delay(
    shipment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    get_shipment_or_404(db, shipment_id)
    return _placeholder_predict("delay")


@router.get("/predict/eta/{shipment_id}")
def predict_eta(
    shipment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("customer", "admin")),
):
    get_shipment_or_404(db, shipment_id)
    return _placeholder_predict("eta")


@router.get("/risk-score/{shipment_id}")
def get_risk_score(
    shipment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    get_shipment_or_404(db, shipment_id)
    return _placeholder_predict("risk_score")
