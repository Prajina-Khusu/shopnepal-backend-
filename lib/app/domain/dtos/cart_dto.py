from pydantic import BaseModel
from typing import List, Optional


class CartItemResponse(BaseModel):
    id:         int
    product_id: int
    quantity:   int

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total: float


class AddToCartRequest(BaseModel):
    product_id: int
    quantity:   int = 1


class UpdateCartRequest(BaseModel):
    quantity: int