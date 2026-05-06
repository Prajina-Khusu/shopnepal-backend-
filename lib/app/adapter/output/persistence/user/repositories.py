from typing import Optional, Dict, Any
from lib.core.db.postgresql.impl import PostgreSQLClient
from lib.core.db.postgresql.models.user import User
from lib.app.domain.repositories import UserRepository


def _to_dict(user: User) -> Dict[str, Any]:
    return {
        "id":         user.id,
        "name":       user.name,
        "email":      user.email,
        "password":   user.password,
        "phone":      user.phone,
        "role":       user.role,
        "is_active":  user.is_active,
        "created_at": user.created_at,
    }


class UserRepositoryImpl(UserRepository):

    def __init__(self, db_client: PostgreSQLClient):
        self.db_client = db_client

    def get_by_email(self, email: str) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            user = db.query(User).filter(User.email == email).first()
            return _to_dict(user) if user else None

    def get_by_id(self, user_id: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            user = db.query(User).filter(User.id == user_id).first()
            return _to_dict(user) if user else None

    def create(self, data: Dict[str, Any]) -> Dict:
        with self.db_client.get_session() as db:
            user = User(**data)
            db.add(user)
            db.flush()
            db.refresh(user)
            return _to_dict(user)