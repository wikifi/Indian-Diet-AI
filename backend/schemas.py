from pydantic import BaseModel, Field


from typing import Optional

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1)
    context_query: Optional[str] = None
    top_k: int = 5


class FoodCalorieRequest(BaseModel):
    food: str
    quantity: float = Field(..., gt=0)


class UserProfile(BaseModel):
    age: int = Field(..., gt=0)
    gender: str
    height_cm: float = Field(..., gt=0)
    weight_kg: float = Field(..., gt=0)
    activity_level: str
    goal: str