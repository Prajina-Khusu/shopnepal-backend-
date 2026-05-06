from typing import Optional, List, Dict, Any
from lib.core.db.postgresql.impl import PostgreSQLClient
from lib.core.db.postgresql.models.review import Review
from lib.app.domain.repositories import ReviewRepository


def _to_dict(r: Review) -> Dict[str, Any]:
    return {
        "id":         r.id,
        "user_id":    r.user_id,
        "product_id": r.product_id,
        "rating":     r.rating,
        "comment":    r.comment,
        "created_at": r.created_at,
    }


class ReviewRepositoryImpl(ReviewRepository):

    def __init__(self, db_client: PostgreSQLClient):
        self.db_client = db_client

    def get_by_product(self, product_id: int) -> List[Dict]:
        with self.db_client.get_session() as db:
            reviews = db.query(Review).filter(
                Review.product_id == product_id
            ).order_by(Review.created_at.desc()).all()
            return [_to_dict(r) for r in reviews]

    def get_by_user_and_product(self, user_id: int, product_id: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            r = db.query(Review).filter(
                Review.user_id    == user_id,
                Review.product_id == product_id
            ).first()
            return _to_dict(r) if r else None

    def create(self, user_id, product_id, rating, comment) -> Dict:
        with self.db_client.get_session() as db:
            review = Review(
                user_id    = user_id,
                product_id = product_id,
                rating     = rating,
                comment    = comment
            )
            db.add(review)
            db.flush()
            db.refresh(review)
            return _to_dict(review)