"""
Shared FastAPI dependencies: current-user extraction and role-based
access control. Every protected route depends on `get_current_user`
(or the `require_role(...)` wrapper) rather than parsing the JWT itself.
"""
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.utils import error_codes
from app.utils.security import decode_token

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error_code": error_codes.AUTH_TOKEN_INVALID, "message": "Invalid or expired token."},
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error_code": error_codes.AUTH_TOKEN_INVALID, "message": "Access token required."},
        )

    user_id = payload.get("sub")
    user = db.get(User, uuid.UUID(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error_code": error_codes.AUTH_TOKEN_INVALID, "message": "User no longer exists."},
        )
    return user


def require_role(*allowed_roles: str):
    """
    Usage: Depends(require_role("admin", "warehouse_staff"))
    Raises 403 if the current user's role isn't in the allowed set.
    """
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error_code": error_codes.PERMISSION_DENIED,
                    "message": f"Requires one of roles: {', '.join(allowed_roles)}.",
                },
            )
        return current_user

    return dependency
