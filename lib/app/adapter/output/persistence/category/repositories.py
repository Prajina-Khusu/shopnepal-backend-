from typing import Optional, List, Dict, Any
from lib.core.db.postgresql.impl import PostgreSQLClient
from lib.core.db.postgresql.models.category import Category
from lib.app.domain.repositories import CategoryRepository


def _to_dict(c: Category) -> Dict[str, Any]:
    return {
        "id":        c.id,
        "name":      c.name,
        "slug":      c.slug,
        "image_url": c.image_url,
        "parent_id": c.parent_id,
    }


class CategoryRepositoryImpl(CategoryRepository):

    def __init__(self, db_client: PostgreSQLClient):
        self.db_client = db_client

    def get_all(self) -> List[Dict]:
        with self.db_client.get_session() as db:
            return [_to_dict(c) for c in db.query(Category).all()]

    def get_by_slug(self, slug: str) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            c = db.query(Category).filter(Category.slug == slug).first()
            return _to_dict(c) if c else None

    def get_by_id(self, category_id: int) -> Optional[Dict]:
        with self.db_client.get_session() as db:
            c = db.query(Category).filter(Category.id == category_id).first()
            return _to_dict(c) if c else None

    def create(self, data: Dict[str, Any]) -> Dict:
        with self.db_client.get_session() as db:
            category = Category(**data)
            db.add(category)
            db.flush()
            db.refresh(category)
            return _to_dict(category)