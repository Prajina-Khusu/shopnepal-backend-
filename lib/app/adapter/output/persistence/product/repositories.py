from typing import Optional, List, Dict, Any
from sqlalchemy import or_
from lib.core.db.postgresql.impl import PostgreSQLClient
from lib.core.db.postgresql.models.product import Product
from lib.app.domain.repositories import ProductRepository


def _to_dict(p: Product) -> Dict[str, Any]:
    return {
        "id":          p.id,
        "name":        p.name,
        "slug":        p.slug,
        "description": p.description,
        "price":       p.price,
        "sale_price":  p.sale_price,
        "stock":       p.stock,
        "is_active":   p.is_active,
        "category_id": p.category_id,
        "seller_id":   p.seller_id,
        "created_at":  p.created_at,
    }


class ProductRepositoryImpl(ProductRepository):

    def __init__(self, db_client: PostgreSQLClient):
        self.db_client = db_client

    def get_all(self, skip, limit, search, category_id) -> List[Dict]:
        with self.db_client.get_session() as db:
            query = db.query(Product).filter(Product.is_active == True)
            if search:
                query = query.filter(
                    or_(
                        Product.name.ilike(f"%{search}%"),
                        Product.description.ilike(f"%{search}%")
                    )
                )
            if category_id:
                query = query.filter(Product.category_id == category_id)
            return [_to_dict(p) for p in query.offset(skip).limit(limit).all()]

    def count(self, search, category_id) -> int:
        with self.db_client.get_session() as db:
            query = db.query(Product).filter(Product.is_active == True)
            if search:
                query = query.filter(
                    or_(
                        Product.name.ilike(f"%{search}%"),
                        Product.description.ilike(f"%{search}%")
                    )
                )
            if category_id:
                query = query.filter(Product.category_id == category_id)
            return query.count()

    def get_by_slug(self, slug: str) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            p = db.query(Product).filter(Product.slug == slug).first()
            return _to_dict(p) if p else None

    def get_by_id(self, product_id: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            p = db.query(Product).filter(Product.id == product_id).first()
            return _to_dict(p) if p else None

    def create(self, data: Dict[str, Any]) -> Dict:
        with self.db_client.get_session() as db:
            product = Product(**data)
            db.add(product)
            db.flush()
            db.refresh(product)
            return _to_dict(product)

    def update(self, product_id: int, data: Dict[str, Any]) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            p = db.query(Product).filter(Product.id == product_id).first()
            if not p:
                return None
            for key, value in data.items():
                setattr(p, key, value)
            db.flush()
            db.refresh(p)
            return _to_dict(p)

    def delete(self, product_id: int) -> bool:
        with self.db_client.get_session() as db:
            p = db.query(Product).filter(Product.id == product_id).first()
            if not p:
                return False
            p.is_active = False
            return True