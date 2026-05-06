from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewResponse(BaseModel):
    id:         int
    user_id:    int
    product_id: int
    rating:     int
    comment:    Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class CreateReviewRequest(BaseModel):
    rating:  int
    comment: Optional[str] = None