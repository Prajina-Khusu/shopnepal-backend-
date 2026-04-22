from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.core.db.postgresql.impl import Base


class Order(Base):
    __tablename__ = "orders"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"))
    status       = Column(String, default="pending")
    total_amount = Column(Float, nullable=False)
    address_id   = Column(Integer, ForeignKey("addresses.id"))
    created_at   = Column(DateTime, default=datetime.utcnow)

    user         = relationship("User",      back_populates="orders")
    items        = relationship("OrderItem", back_populates="order")
    address      = relationship("Address")


class OrderItem(Base):
    __tablename__ = "order_items"

    id         = Column(Integer, primary_key=True, index=True)
    order_id   = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity   = Column(Integer, nullable=False)
    price      = Column(Float, nullable=False)

    order      = relationship("Order",   back_populates="items")
    product    = relationship("Product", back_populates="order_items")