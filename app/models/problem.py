from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    difficulty = Column(String(10), nullable=False)  # easy, medium, hard

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())

    categories = relationship("ProblemCategory", back_populates="problem", cascade="all, delete")
