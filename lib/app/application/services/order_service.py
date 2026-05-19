from typing import List
from fastapi import HTTPException, status
from lib.app.domain.services.base import OrderServiceBase
from lib.app.domain.repositories import OrderRepository, CartRepository, AddressRepository
from lib.app.domain.dtos.order_dto import (
    OrderResponse, CheckoutRequest, UpdateOrderStatusRequest
)
from lib.core.utils.enums import OrderStatus


class OrderService(OrderServiceBase):

    def __init__(
        self,
        order_repository:   OrderRepository,
        cart_repository:    CartRepository,
        address_repository: AddressRepository,       # ← add this
    ):
        self.order_repository   = order_repository
        self.cart_repository    = cart_repository
        self.address_repository = address_repository  # ← add this

    async def checkout(
        self,
        user_id: int,
        request: CheckoutRequest
    ) -> OrderResponse:

        # ── 1. Validate address belongs to this user ──────────────────
        address = self.address_repository.get_by_id(request.address_id)
        if not address:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Address {request.address_id} not found. "
                       "Create an address first via POST /api/v1/addresses/"
            )
        if address["user_id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="That address does not belong to you"
            )

        # ── 2. Validate cart is not empty ─────────────────────────────
        cart_items = self.cart_repository.get_by_user(user_id)
        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty"
            )

        # ── 3. Build items + total ─────────────────────────────────────
        items = []
        total = 0.0
        for item in cart_items:
            # Defensive: support both ORM objects and dicts
            if isinstance(item, dict):
                price      = item.get("sale_price") or item.get("price") or 0
                product_id = item["product_id"]
                quantity   = item["quantity"]
            else:
                price      = getattr(item, "sale_price", None) or getattr(item, "price", 0)
                product_id = item.product_id
                quantity   = item.quantity

            total += float(price) * int(quantity)
            items.append({
                "product_id": product_id,
                "quantity":   quantity,
                "price":      price,
            })

        # ── 4. Create order ───────────────────────────────────────────
        order = self.order_repository.create(
            user_id    = user_id,
            address_id = request.address_id,
            items      = items,
            total      = round(total, 2)
        )
        self.cart_repository.clear_cart(user_id)
        return OrderResponse(**order)

    # ── remaining methods unchanged ───────────────────────────────────

    async def get_orders(self, user_id: int) -> List[OrderResponse]:
        orders = self.order_repository.get_by_user(user_id)
        return [OrderResponse(**o) for o in orders]

    async def get_order(self, order_id: int) -> OrderResponse:
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return OrderResponse(**order)

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
        return OrderResponse(**order)