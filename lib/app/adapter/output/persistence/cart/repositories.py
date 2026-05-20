from typing import Optional, List, Dict, Any
from lib.core.db.postgresql.impl import PostgreSQLClient
from lib.core.db.postgresql.models.cart import Cart
from lib.app.domain.repositories import CartRepository


def _to_dict(c: Cart) -> Dict[str, Any]:
    return {
        "id":         c.id,
        "user_id":    c.user_id,
        "product_id": c.product_id,
        "quantity":   c.quantity,
    }


class CartRepositoryImpl(CartRepository):

    def __init__(self, db_client: PostgreSQLClient):
        self.db_client = db_client

    def get_by_user(self, user_id: int) -> List[Dict]:
        with self.db_client.get_session() as db:from typing import Optional, List, Dict, Any
from lib.core.db.postgresql.impl import PostgreSQLClient
from lib.core.db.postgresql.models.cart import Cart
from lib.core.db.postgresql.models.product import Product
from lib.app.domain.repositories import CartRepository


def _to_dict(c: Cart, product: Product = None) -> Dict[str, Any]:
    return {
        "id":         c.id,
        "user_id":    c.user_id,
        "product_id": c.product_id,
        "quantity":   c.quantity,
        # include price from joined product so order_service can calculate total
        "price":      product.price      if product else 0,
        "sale_price": product.sale_price if product else None,
        "name":       product.name       if product else None,
    }


class CartRepositoryImpl(CartRepository):

    def __init__(self, db_client: PostgreSQLClient):
        self.db_client = db_client

    def get_by_user(self, user_id: int) -> List[Dict]:
        with self.db_client.get_session() as db:
            rows = (
                db.query(Cart, Product)
                .join(Product, Cart.product_id == Product.id)
                .filter(Cart.user_id == user_id)
                .all()
            )
            return [_to_dict(cart, product) for cart, product in rows]

    def get_item(self, user_id: int, product_id: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            row = (
                db.query(Cart, Product)
                .join(Product, Cart.product_id == Product.id)
                .filter(Cart.user_id == user_id, Cart.product_id == product_id)
                .first()
            )
            return _to_dict(row[0], row[1]) if row else None

    def get_item_by_id(self, item_id: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            row = (
                db.query(Cart, Product)
                .join(Product, Cart.product_id == Product.id)
                .filter(Cart.id == item_id)
                .first()
            )
            return _to_dict(row[0], row[1]) if row else None

    def add_item(self, user_id: int, product_id: int, quantity: int) -> Dict:
        with self.db_client.get_session() as db:
            item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
            db.add(item)
            db.flush()
            db.refresh(item)
            product = db.query(Product).filter(Product.id == product_id).first()
            return _to_dict(item, product)

    def update_item(self, item_id: int, quantity: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            item = db.query(Cart).filter(Cart.id == item_id).first()
            if not item:
                return None
            item.quantity = quantity
            db.flush()
            db.refresh(item)
            product = db.query(Product).filter(Product.id == item.product_id).first()
            return _to_dict(item, product)

    def remove_item(self, item_id: int) -> bool:
        with self.db_client.get_session() as db:
            item = db.query(Cart).filter(Cart.id == item_id).first()
            if not item:
                return False
            db.delete(item)
            return True

    def clear_cart(self, user_id: int) -> bool:
        with self.db_client.get_session() as db:
            db.query(Cart).filter(Cart.user_id == user_id).delete()
            return True
            items = db.query(Cart).filter(Cart.user_id == user_id).all()
            return [_to_dict(i) for i in items]

    def get_item(self, user_id: int, product_id: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            item = db.query(Cart).filter(
                Cart.user_id    == user_id,
                Cart.product_id == product_id
            ).first()
            return _to_dict(item) if item else None

    def get_item_by_id(self, item_id: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            item = db.query(Cart).filter(Cart.id == item_id).first()
            return _to_dict(item) if item else None

    def add_item(self, user_id: int, product_id: int, quantity: int) -> Dict:
        with self.db_client.get_session() as db:
            item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
            db.add(item)
            db.flush()
            db.refresh(item)
            return _to_dict(item)

    def update_item(self, item_id: int, quantity: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            item = db.query(Cart).filter(Cart.id == item_id).first()
            if not item:
                return None
            item.quantity = quantity
            db.flush()
            db.refresh(item)
            return _to_dict(item)

    def remove_item(self, item_id: int) -> bool:
        with self.db_client.get_session() as db:
            item = db.query(Cart).filter(Cart.id == item_id).first()
            if not item:
                return False
            db.delete(item)
            return True

    def clear_cart(self, user_id: int) -> bool:
        with self.db_client.get_session() as db:
            db.query(Cart).filter(Cart.user_id == user_id).delete()
            return True