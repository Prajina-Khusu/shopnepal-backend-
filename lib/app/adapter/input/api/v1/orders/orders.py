from fastapi import APIRouter, Depends
from typing import List
from dependency_injector.wiring import Provide, inject
from lib.app.container import Container
from lib.app.application.services.order_service import OrderService
from lib.app.domain.dtos.order_dto import (
    OrderResponse, CheckoutRequest, UpdateOrderStatusRequest
)
from lib.app.adapter.input.api.v1.dependencies.auth import (
    get_current_user, get_current_admin
)
from lib.app.domain.dtos.auth_dto import UserResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/checkout", response_model=OrderResponse, status_code=201)
@inject
async def checkout(
    request:      CheckoutRequest,
    current_user: UserResponse = Depends(get_current_user),
    service:      OrderService = Depends(Provide[Container.order_service])
):
    return await service.checkout(current_user.id, request)


@router.get("/", response_model=List[OrderResponse])
@inject
async def get_orders(
    current_user: UserResponse = Depends(get_current_user),
    service:      OrderService = Depends(Provide[Container.order_service])
):
    return await service.get_orders(current_user.id)


@router.get("/{order_id}", response_model=OrderResponse)
@inject
async def get_order(
    order_id:     int,
    current_user: UserResponse = Depends(get_current_user),
    service:      OrderService = Depends(Provide[Container.order_service])
):
    return await service.get_order(order_id)


@router.patch("/{order_id}/status", response_model=OrderResponse)
@inject
async def update_order_status(
    order_id:     int,
    request:      UpdateOrderStatusRequest,
    current_user: UserResponse = Depends(get_current_admin),
    service:      OrderService = Depends(Provide[Container.order_service])
):
    return await service.update_status(order_id, request)