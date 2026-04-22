from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.core.db.postgresql.impl import Base


class Review(Base):
    __tablename__ = "reviews"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    rating     = Column(Integer, nullable=False)
    comment    = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user       = relationship("User",    back_populates="reviews")
    product    = relationship("Product", back_populates="reviews")