from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.problem import ProblemOut
from app.utils.jwt import get_current_user
from app.models.user import User

from app.services.problem_service import get_personalized_feed


router = APIRouter(prefix="/problems", tags=["Problems"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/feed", response_model=list[ProblemOut])
def get_feed(
    difficulty: str = Query(None, pattern="^(easy|medium|hard)$"),
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_personalized_feed(
        db=db,
        user_id=current_user.id,
        difficulty=difficulty,
        limit=limit
    )