from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.core.db.postgresql.impl import Base


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        UniqueConstraint("slug", "seller_id", name="uq_product_slug_seller"),  # ← unique per seller
    )

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    slug        = Column(String, index=True)          # ← removed global unique=True
    description = Column(String)
    price       = Column(Float, nullable=False)
    sale_price  = Column(Float)
    stock       = Column(Integer, default=0)
    is_active   = Column(Boolean, default=True)
    created_at  = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    seller_id   = Column(Integer, ForeignKey("users.id"), nullable=True)

    category    = relationship("Category",     back_populates="products")
    images      = relationship("ProductImage", back_populates="product")
    order_items = relationship("OrderItem",    back_populates="product")
    cart_items  = relationship("Cart",         back_populates="product")
    reviews     = relationship("Review",       back_populates="product")


class ProductImage(Base):
    __tablename__ = "product_images"

    id         = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    image_url  = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)

    product    = relationship("Product", back_populates="images")