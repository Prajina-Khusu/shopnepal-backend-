from abc import ABC, abstractmethod
from typing import Optional, List
from lib.app.domain.dtos import *


class AuthServiceBase(ABC):

    @abstractmethod
    async def register(self, request: RegisterRequest) -> UserResponse:
        pass

    @abstractmethod
    async def login(self, request: LoginRequest) -> TokenResponse:
        pass

    @abstractmethod
    async def get_current_user(self, token: str) -> UserResponse:
        pass


class ProductServiceBase(ABC):

    @abstractmethod
    async def get_all(self, request: ProductListRequest) -> ProductListResponse:
        pass

    @abstractmethod
    async def get_by_slug(self, slug: str) -> ProductResponse:
        pass

    @abstractmethod
    async def create(self, request: CreateProductRequest) -> ProductResponse:
        pass

    @abstractmethod
    async def update(
        self,
        product_id: int,
        request: UpdateProductRequest
    ) -> ProductResponse:
        pass

    @abstractmethod
    async def delete(self, product_id: int) -> bool:
        pass


class CategoryServiceBase(ABC):

    @abstractmethod
    async def get_all(self) -> List[CategoryResponse]:
        pass

    @abstractmethod
    async def create(self, request: CreateCategoryRequest) -> CategoryResponse:
        pass


class CartServiceBase(ABC):

    @abstractmethod
    async def get_cart(self, user_id: int) -> CartResponse:
        pass

    @abstractmethod
    async def add_item(
        self,
        user_id: int,
        request: AddToCartRequest
    ) -> CartResponse:
        pass

    @abstractmethod
    async def update_item(
        self,
        user_id: int,
        item_id: int,
        request: UpdateCartRequest
    ) -> CartResponse:
        pass

    @abstractmethod
    async def remove_item(self, user_id: int, item_id: int) -> bool:
        pass


class OrderServiceBase(ABC):

    @abstractmethod
    async def checkout(
        self,
        user_id: int,
        request: CheckoutRequest
    ) -> OrderResponse:
        pass

    @abstractmethod
    async def get_orders(self, user_id: int) -> List[OrderResponse]:
        pass

    @abstractmethod
    async def get_order(self, order_id: int) -> OrderResponse:
        pass

    @abstractmethod
    async def update_status(
        self,
        order_id: int,
        request: UpdateOrderStatusRequest
    ) -> OrderResponse:
        pass


class ReviewServiceBase(ABC):

    @abstractmethod
    async def get_reviews(self, product_id: int) -> List[ReviewResponse]:
        pass

    @abstractmethod
    async def create(
        self,
        user_id: int,
        product_id: int,
        request: CreateReviewRequest
    ) -> ReviewResponse:
        pass