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
        with self.db_client.get_session() as db:
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