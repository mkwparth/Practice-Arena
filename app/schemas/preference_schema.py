from pydantic import BaseModel
from typing import List


class PreferenceRequest(BaseModel):
    category_ids: List[int]


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True