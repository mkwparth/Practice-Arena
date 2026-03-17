from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class ProblemCategory(Base):
    __tablename__ = "problem_categories"

    id = Column(Integer, primary_key=True)

    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))

    problem = relationship("Problem", back_populates="categories")
    category = relationship("Category")

    __table_args__ = (
        UniqueConstraint("problem_id", "category_id", name="unique_problem_category"),
    )