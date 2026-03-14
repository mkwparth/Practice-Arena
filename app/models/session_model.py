import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func
from app.db.base import Base

class Session(Base):

    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    refresh_token = Column(String)

    expires_at = Column(DateTime)

    created_at = Column(DateTime, default=func.now())