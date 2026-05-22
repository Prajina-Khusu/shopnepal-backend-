from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.core.db.postgresql.impl import Base


class SellerApplication(Base):
    __tablename__ = "seller_applications"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), unique=True)
    shop_name    = Column(String, nullable=False, unique=True)   # ← unique shop name
    shop_address = Column(String, nullable=False)
    phone        = Column(String, nullable=False)
    description  = Column(String)
    status       = Column(String, default="pending")
    created_at   = Column(DateTime, default=datetime.utcnow)
    reviewed_at  = Column(DateTime, nullable=True)
    reviewed_by  = Column(Integer, ForeignKey("users.id"), nullable=True)

    user         = relationship("User", foreign_keys=[user_id])
    reviewer     = relationship("User", foreign_keys=[reviewed_by])