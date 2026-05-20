from typing import Optional, List, Dict, Any
from datetime import datetime
from lib.core.db.postgresql.impl import PostgreSQLClient
from lib.core.db.postgresql.models.seller_application import SellerApplication
from lib.core.db.postgresql.models.user import User


def _to_dict(s: SellerApplication) -> Dict[str, Any]:
    return {
        "id":           s.id,
        "user_id":      s.user_id,
        "shop_name":    s.shop_name,
        "shop_address": s.shop_address,
        "phone":        s.phone,
        "description":  s.description,
        "status":       s.status,
        "created_at":   s.created_at,
        "reviewed_at":  s.reviewed_at,
        "reviewed_by":  s.reviewed_by,
    }


class SellerRepositoryImpl:

    def __init__(self, db_client: PostgreSQLClient):
        self.db_client = db_client

    def get_by_user(self, user_id: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            s = db.query(SellerApplication).filter(
                SellerApplication.user_id == user_id
            ).first()
            return _to_dict(s) if s else None

    def get_all(self, status: Optional[str] = None) -> List[Dict]:
        with self.db_client.get_session() as db:
            query = db.query(SellerApplication)
            if status:
                query = query.filter(SellerApplication.status == status)
            return [_to_dict(s) for s in query.all()]

    def get_by_id(self, application_id: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            s = db.query(SellerApplication).filter(
                SellerApplication.id == application_id
            ).first()
            return _to_dict(s) if s else None

    def create(self, user_id: int, data: Dict[str, Any]) -> Dict:
        with self.db_client.get_session() as db:
            application = SellerApplication(user_id=user_id, **data)
            db.add(application)
            db.flush()
            db.refresh(application)
            return _to_dict(application)

    def update_status(
        self,
        application_id: int,
        status:         str,
        reviewed_by:    int
    ) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            s = db.query(SellerApplication).filter(
                SellerApplication.id == application_id
            ).first()
            if not s:
                return None
            s.status      = status
            s.reviewed_by = reviewed_by
            s.reviewed_at = datetime.utcnow()
            db.flush()
            db.refresh(s)
            return _to_dict(s)

    def update_user_role(self, user_id: int, role: str) -> bool:
        with self.db_client.get_session() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            user.role = role
            return True