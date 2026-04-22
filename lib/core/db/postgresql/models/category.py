from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from lib.core.db.postgresql.impl import Base


class Category(Base):
    __tablename__ = "categories"

    id        = Column(Integer, primary_key=True, index=True)
    name      = Column(String, nullable=False)
    slug      = Column(String, unique=True, index=True)
    image_url = Column(String)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    products  = relationship("Product", back_populates="category")