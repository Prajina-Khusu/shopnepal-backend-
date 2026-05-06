from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from lib.core.db.postgresql.impl import Base


class Address(Base):
    __tablename__ = "addresses"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"))
    full_name  = Column(String, nullable=False)
    phone      = Column(String, nullable=False)
    street     = Column(String, nullable=False)
    city       = Column(String, nullable=False)
    province   = Column(String, nullable=False)
    is_default = Column(Boolean, default=False)

    user       = relationship("User", back_populates="addresses")