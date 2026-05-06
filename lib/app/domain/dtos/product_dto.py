from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProductResponse(BaseModel):
    id:          int
    name:        str
    slug:        str
    description: Optional[str]
    price:       float
    sale_price:  Optional[float]
    stock:       int
    is_active:   bool
    category_id: Optional[int]
    created_at:  datetime

    class Config:
        from_attributes = True


class CreateProductRequest(BaseModel):
    name:        str
    description: Optional[str] = None
    price:       float
    sale_price:  Optional[float] = None
    stock:       int             = 0
    category_id: Optional[int]  = None


class UpdateProductRequest(BaseModel):
    name:        Optional[str]   = None
    description: Optional[str]   = None
    price:       Optional[float] = None
    sale_price:  Optional[float] = None
    stock:       Optional[int]   = None
    is_active:   Optional[bool]  = None


class ProductListRequest(BaseModel):
    skip:        int            = 0
    limit:       int            = 20
    search:      Optional[str]  = None
    category_id: Optional[int]  = None


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    skip:  int
    limit: int