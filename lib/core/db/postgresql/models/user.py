from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.core.db.postgresql.impl import Base


class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String, nullable=False)
    email      = Column(String, unique=True, index=True, nullable=False)
    password   = Column(String, nullable=False)
    phone      = Column(String)
    role       = Column(String, default="customer")
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders    = relationship("Order",   back_populates="user")
    cart      = relationship("Cart",    back_populates="user")
    reviews   = relationship("Review",  back_populates="user")
    addresses = relationship("Address", back_populates="user")