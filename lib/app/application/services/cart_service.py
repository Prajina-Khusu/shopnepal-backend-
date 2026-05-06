from fastapi import HTTPException, status
from lib.app.domain.services.base import CartServiceBase
from lib.app.domain.repositories import CartRepository, ProductRepository
from lib.app.domain.dtos.cart_dto import (
    CartResponse, CartItemResponse,
    AddToCartRequest, UpdateCartRequest
)


class CartService(CartServiceBase):

    def __init__(
        self,
        cart_repository:    CartRepository,
        product_repository: ProductRepository
    ):
        self.cart_repository    = cart_repository
        self.product_repository = product_repository

    def _build_response(self, user_id: int) -> CartResponse:
        items = self.cart_repository.get_by_user(user_id)
        total = 0.0
        for item in items:
            product = self.product_repository.get_by_id(item.product_id)
            if product:
                price  = product.sale_price or product.price
                total += price * item.quantity
        return CartResponse(
            items = [CartItemResponse.model_validate(i) for i in items],
            total = round(total, 2)
        )

    async def get_cart(self, user_id: int) -> CartResponse:
        return self._build_response(user_id)

    async def add_item(
        self,
        user_id: int,
        request: AddToCartRequest
    ) -> CartResponse:
        product = self.product_repository.get_by_id(request.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        if product.stock < request.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )
        existing = self.cart_repository.get_item(user_id, request.product_id)
        if existing:
            self.cart_repository.update_item(
                existing.id,
                existing.quantity + request.quantity
            )
        else:
            self.cart_repository.add_item(
                user_id    = user_id,
                product_id = request.product_id,
                quantity   = request.quantity
            )
        return self._build_response(user_id)

    async def update_item(
        self,
        user_id: int,
        item_id: int,
        request: UpdateCartRequest
    ) -> CartResponse:
        item = self.cart_repository.get_item_by_id(item_id)
        if not item or item.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
        self.cart_repository.update_item(item_id, request.quantity)
        return self._build_response(user_id)

    async def remove_item(self, user_id: int, item_id: int) -> bool:
        item = self.cart_repository.get_item_by_id(item_id)
        if not item or item.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
        return self.cart_repository.remove_item(item_id)