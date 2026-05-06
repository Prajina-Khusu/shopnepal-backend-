from typing import Optional, List, Dict, Any
from lib.core.db.postgresql.impl import PostgreSQLClient
from lib.core.db.postgresql.models.order import Order, OrderItem
from lib.app.domain.repositories import OrderRepository


def _item_to_dict(i: OrderItem) -> Dict[str, Any]:
    return {
        "id":         i.id,
        "order_id":   i.order_id,
        "product_id": i.product_id,
        "quantity":   i.quantity,
        "price":      i.price,
    }


def _to_dict(o: Order, items: List[OrderItem] = []) -> Dict[str, Any]:
    return {
        "id":           o.id,
        "user_id":      o.user_id,
        "status":       o.status,
        "total_amount": o.total_amount,
        "address_id":   o.address_id,
        "created_at":   o.created_at,
        "items":        [_item_to_dict(i) for i in items],
    }


class OrderRepositoryImpl(OrderRepository):

    def __init__(self, db_client: PostgreSQLClient):
        self.db_client = db_client

    def create(self, user_id, address_id, items, total) -> Dict:
        with self.db_client.get_session() as db:
            order = Order(
                user_id      = user_id,
                address_id   = address_id,
                total_amount = total,
                status       = "pending"
            )
            db.add(order)
            db.flush()
            order_items = []
            for item in items:
                oi = OrderItem(
                    order_id   = order.id,
                    product_id = item["product_id"],
                    quantity   = item["quantity"],
                    price      = item["price"]
                )
                db.add(oi)
                order_items.append(oi)
            db.flush()
            return _to_dict(order, order_items)

    def get_by_user(self, user_id: int) -> List[Dict]:
        with self.db_client.get_session() as db:
            orders = db.query(Order).filter(
                Order.user_id == user_id
            ).order_by(Order.created_at.desc()).all()
            result = []
            for o in orders:
                items = db.query(OrderItem).filter(OrderItem.order_id == o.id).all()
                result.append(_to_dict(o, items))
            return result

    def get_by_id(self, order_id: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            o = db.query(Order).filter(Order.id == order_id).first()
            if not o:
                return None
            items = db.query(OrderItem).filter(OrderItem.order_id == o.id).all()
            return _to_dict(o, items)

    def update_status(self, order_id: int, status: str) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            o = db.query(Order).filter(Order.id == order_id).first()
            if not o:
                return None
            o.status = status
            db.flush()
            items = db.query(OrderItem).filter(OrderItem.order_id == o.id).all()
            return _to_dict(o, items)