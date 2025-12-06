from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class ReviewCreate(BaseModel):
    vehicle: int = Field(..., ge=1, le=4)
    driver: int = Field(..., ge=1, le=4)
    guide: int = Field(..., ge=1, le=4)
    accommodation: int = Field(..., ge=1, le=4)
    meals: int = Field(..., ge=1, le=4)

    comment: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    tour_id: Optional[str] = None


class ReviewOut(ReviewCreate):
    id: int
    overall_score: Optional[float]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ReviewStats(BaseModel):
    avg_vehicle: float
    avg_driver: float
    avg_guide: float
    avg_accommodation: float
    avg_meals: float
    avg_overall: float

    total_reviews: int


class ReviewsWithStats(BaseModel):
    stats: ReviewStats
    reviews: list[ReviewOut]
