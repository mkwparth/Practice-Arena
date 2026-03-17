from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserAttempt(Base):

    __tablename__ = "user_attempts"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"))

    status = Column(String, default="served")  # served, attempted, solved, skipped

    attempt_count = Column(Integer, default=0)

    first_served_at = Column(DateTime, default=func.now())
    last_attempted_at = Column(DateTime, nullable=True)
    solved_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship("User")
    problem = relationship("Problem")

    __table_args__ = (
        UniqueConstraint("user_id", "problem_id", name="unique_user_problem"),
    )