from typing import Optional, List, Dict, Any
from lib.core.db.postgresql.impl import PostgreSQLClient
from lib.core.db.postgresql.models.address import Address
from lib.app.domain.repositories import AddressRepository


def _to_dict(a: Address) -> Dict[str, Any]:
    return {
        "id":         a.id,
        "user_id":    a.user_id,
        "full_name":  a.full_name,
        "phone":      a.phone,
        "street":     a.street,
        "city":       a.city,
        "province":   a.province,
        "is_default": a.is_default,
    }


class AddressRepositoryImpl(AddressRepository):

    def __init__(self, db_client: PostgreSQLClient):
        self.db_client = db_client

    def get_by_id(self, address_id: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            a = db.query(Address).filter(Address.id == address_id).first()
            return _to_dict(a) if a else None

    def get_by_user(self, user_id: int) -> List[Dict]:
        with self.db_client.get_session() as db:
            addresses = db.query(Address).filter(
                Address.user_id == user_id
            ).all()
            return [_to_dict(a) for a in addresses]

    def create(self, user_id: int, data: dict) -> Dict:
        with self.db_client.get_session() as db:
            # If this is set as default, unset all others first
            if data.get("is_default"):
                db.query(Address).filter(
                    Address.user_id == user_id
                ).update({"is_default": False})

            a = Address(
                user_id    = user_id,
                full_name  = data["full_name"],
                phone      = data["phone"],
                street     = data["street"],
                city       = data["city"],
                province   = data["province"],
                is_default = data.get("is_default", False),
            )
            db.add(a)
            db.flush()
            return _to_dict(a)