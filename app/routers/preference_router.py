from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.preference_schema import PreferenceRequest
from app.services.preference_service import (
    save_user_preferences,
    get_user_preferences,
    get_all_categories
)

from app.models.user import User
from app.utils.jwt import get_current_user

router = APIRouter(prefix="/preferences", tags=["Preferences"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/categories")
def categories(db: Session = Depends(get_db)):
    return get_all_categories(db)


@router.post("/")
def save_preferences(
    data: PreferenceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    save_user_preferences(db, current_user.id, data.category_ids)

    return {"message": "Preferences saved successfully"}


@router.get("/")
def my_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_user_preferences(db, current_user.id)


@router.put("/")
def update_preferences(
    data: PreferenceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    save_user_preferences(db, current_user.id, data.category_ids)

    return {"message": "Preferences updated"}