from pydantic import BaseModel
from typing import Optional


class AddressCreateRequest(BaseModel):
    full_name:  str
    phone:      str
    street:     str
    city:       str
    province:   str
    is_default: Optional[bool] = False


class AddressResponse(BaseModel):
    id:         int
    user_id:    int
    full_name:  str
    phone:      str
    street:     str
    city:       str
    province:   str
    is_default: bool

    class Config:
        from_attributes = True