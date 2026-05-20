from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SellerApplicationRequest(BaseModel):
    shop_name:    str
    shop_address: str
    phone:        str
    description:  Optional[str] = None


class SellerApplicationResponse(BaseModel):
    id:           int
    user_id:      int
    shop_name:    str
    shop_address: str
    phone:        str
    description:  Optional[str]
    status:       str
    created_at:   datetime

    class Config:
        from_attributes = True


class ReviewApplicationRequest(BaseModel):
    status: str  # approved / rejected