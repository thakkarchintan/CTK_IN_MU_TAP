from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, CurrentUser
from app.services.auth_service import login
from app.api.deps import get_current_user
from app.models.models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login_route(payload: LoginRequest, db: Session = Depends(get_db)):
    token = login(db, payload.email, payload.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return TokenResponse(access_token=token)


@router.get("/me", response_model=CurrentUser)
def me_route(current_user: User = Depends(get_current_user)):
    return CurrentUser(id=current_user.id, email=current_user.email)
