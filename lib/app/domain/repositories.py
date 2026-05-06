from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class UserRepository(ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Any]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Any:
        pass


class ProductRepository(ABC):

    @abstractmethod
    def get_all(
        self,
        skip: int,
        limit: int,
        search: Optional[str],
        category_id: Optional[int]
    ) -> List[Any]:
        pass

    @abstractmethod
    def count(
        self,
        search: Optional[str],
        category_id: Optional[int]
    ) -> int:
        pass

    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[Any]:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def update(self, product_id: int, data: Dict[str, Any]) -> Optional[Any]:
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        pass


class CategoryRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Any]:
        pass

    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[Any]:
        pass

    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Any:
        pass


class CartRepository(ABC):

    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Any]:
        pass

    @abstractmethod
    def get_item(self, user_id: int, product_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def get_item_by_id(self, item_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def add_item(self, user_id: int, product_id: int, quantity: int) -> Any:
        pass

    @abstractmethod
    def update_item(self, item_id: int, quantity: int) -> Optional[Any]:
        pass

    @abstractmethod
    def remove_item(self, item_id: int) -> bool:
        pass

    @abstractmethod
    def clear_cart(self, user_id: int) -> bool:
        pass


class OrderRepository(ABC):

    @abstractmethod
    def create(
        self,
        user_id: int,
        address_id: int,
        items: List[Dict],
        total: float
    ) -> Any:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> List[Any]:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def update_status(self, order_id: int, status: str) -> Optional[Any]:
        pass


class ReviewRepository(ABC):

    @abstractmethod
    def get_by_product(self, product_id: int) -> List[Any]:
        pass

    @abstractmethod
    def get_by_user_and_product(
        self,
        user_id: int,
        product_id: int
    ) -> Optional[Any]:
        pass

    @abstractmethod
    def create(
        self,
        user_id: int,
        product_id: int,
        rating: int,
        comment: str
    ) -> Any:
        pass