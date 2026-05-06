from typing import List
from fastapi import HTTPException, status
from lib.app.domain.services.base import OrderServiceBase
from lib.app.domain.repositories import OrderRepository, CartRepository
from lib.app.domain.dtos.order_dto import (
    OrderResponse, CheckoutRequest, UpdateOrderStatusRequest
)
from lib.core.utils.enums import OrderStatus


class OrderService(OrderServiceBase):

    def __init__(
        self,
        order_repository: OrderRepository,
        cart_repository:  CartRepository
    ):
        self.order_repository = order_repository
        self.cart_repository  = cart_repository

    async def checkout(
        self,
        user_id: int,
        request: CheckoutRequest
    ) -> OrderResponse:
        cart_items = self.cart_repository.get_by_user(user_id)
        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty"
            )
        items = []
        total = 0.0
        for item in cart_items:
            price  = item.product.sale_price or item.product.price
            total += price * item.quantity
            items.append({
                "product_id": item.product_id,
                "quantity":   item.quantity,
                "price":      price
            })
        order = self.order_repository.create(
            user_id    = user_id,
            address_id = request.address_id,
            items      = items,
            total      = round(total, 2)
        )
        self.cart_repository.clear_cart(user_id)
        return OrderResponse.model_validate(order)

    async def get_orders(self, user_id: int) -> List[OrderResponse]:
        orders = self.order_repository.get_by_user(user_id)
        return [OrderResponse.model_validate(o) for o in orders]

    async def get_order(self, order_id: int) -> OrderResponse:
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return OrderResponse.model_validate(order)

    async def update_status(
        self,
        order_id: int,
        request: UpdateOrderStatusRequest
    ) -> OrderResponse:
        if request.status not in [s.value for s in OrderStatus]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {[s.value for s in OrderStatus]}"
            )
        order = self.order_repository.update_status(order_id, request.status)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return OrderResponse.model_validate(order)