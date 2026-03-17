# app/schemas/problem.py

from pydantic import BaseModel

class ProblemOut(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str

    class Config:
        from_attributes = True   # ✅ important (Pydantic v2)