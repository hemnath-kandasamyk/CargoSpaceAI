"""Business logic for registration and login — kept out of the route
handlers so it can be unit-tested without spinning up FastAPI."""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest
from app.utils import error_codes
from app.utils.security import create_access_token, create_refresh_token, hash_password, verify_password


def register_user(db: Session, payload: RegisterRequest) -> User:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error_code": error_codes.DUPLICATE_RESOURCE, "message": "Email already registered."},
        )

    role = db.query(Role).filter(Role.name == payload.role).first()
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": error_codes.VALIDATION_ERROR, "message": f"Unknown role '{payload.role}'."},
        )

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role_id=role.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, payload: LoginRequest) -> User:
    user = db.query(User).filter(User.email == payload.email).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error_code": error_codes.AUTH_INVALID_CREDENTIALS, "message": "Invalid email or password."},
        )
    return user


def issue_tokens(user: User) -> tuple[str, str]:
    access_token = create_access_token(user.id, user.role.name)
    refresh_token = create_refresh_token(user.id, user.role.name)
    return access_token, refresh_token
