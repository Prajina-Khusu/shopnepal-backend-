from enum import Enum


class UserRole(str, Enum):
    customer = "customer"
    seller   = "seller"
    admin    = "admin"


class OrderStatus(str, Enum):
    pending    = "pending"
    processing = "processing"
    shipped    = "shipped"
    delivered  = "delivered"
    cancelled  = "cancelled"