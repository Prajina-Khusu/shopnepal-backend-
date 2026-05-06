from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderItemResponse(BaseModel):
    product_id: int
    quantity:   int
    price:      float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id:           int
    status:       str
    total_amount: float
    created_at:   datetime
    items:        List[OrderItemResponse] = []

    class Config:
        from_attributes = True


class CheckoutRequest(BaseModel):
    address_id: int


class UpdateOrderStatusRequest(BaseModel):
    status: str