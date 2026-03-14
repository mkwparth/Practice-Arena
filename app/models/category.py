from sqlalchemy import Column, String, Boolean, Integer
from app.db.base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)