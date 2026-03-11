import uuid
from sqlalchemy import Column, String, ForeignKey
from app.db.base import Base

class AuthAccount(Base):

    __tablename__ = "auth_accounts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, ForeignKey("users.id"))

    provider = Column(String)
    provider_user_id = Column(String)

    password_hash = Column(String)