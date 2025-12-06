from datetime import datetime
from typing import Optional, Dict

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
    """
    Статистика для dashboard:
    - total: общее количество отзывов
    - averages: средние оценки по категориям
    - distribution: распределение оценок {1: count, 2: count, 3: count, 4: count}
    """
    total: int
    averages: Dict[str, float]  # {"vehicle": 3.5, "driver": 3.8, ...}
    distribution: Dict[str, Dict[int, int]]  # {"vehicle": {1: 5, 2: 10, ...}, ...}


class ReviewsWithStats(BaseModel):
    stats: ReviewStats
    reviews: list[ReviewOut]