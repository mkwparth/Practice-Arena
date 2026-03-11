from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.auth_schema import RegisterRequest, LoginRequest, RefreshRequest
from app.services.auth_service import register_user, login_user, refresh_access_token

from app.db.session import SessionLocal

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    user = register_user(
        db,
        data.email,
        data.password,
        data.name
    )

    return {
        "message": "User created",
        "user_id": user.id
    }


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    result = login_user(
        db,
        data.email,
        data.password
    )

    if not result:
        return {"error": "Invalid credentials"}

    access, refresh = result

    return {
        "access_token": access,
        "refresh_token": refresh
    }


@router.post("/refresh")
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):

    access_token = refresh_access_token(
        db,
        data.refresh_token
    )

    if not access_token:
        return {"error": "Invalid refresh token"}

    return {"access_token": access_token}