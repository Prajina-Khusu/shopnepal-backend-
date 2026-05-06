from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from lib.app.container import Container
from lib.app.application.services.cart_service import CartService
from lib.app.domain.dtos.cart_dto import (
    CartResponse, AddToCartRequest, UpdateCartRequest
)
from lib.app.adapter.input.api.v1.dependencies.auth import get_current_user
from lib.app.domain.dtos.auth_dto import UserResponse

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=CartResponse)
@inject
async def get_cart(
    current_user: UserResponse = Depends(get_current_user),
    service:      CartService  = Depends(Provide[Container.cart_service])
):
    return await service.get_cart(current_user.id)


@router.post("/", response_model=CartResponse, status_code=201)
@inject
async def add_to_cart(
    request:      AddToCartRequest,
    current_user: UserResponse = Depends(get_current_user),
    service:      CartService  = Depends(Provide[Container.cart_service])
):
    return await service.add_item(current_user.id, request)


@router.put("/{item_id}", response_model=CartResponse)
@inject
async def update_cart_item(
    item_id:      int,
    request:      UpdateCartRequest,
    current_user: UserResponse = Depends(get_current_user),
    service:      CartService  = Depends(Provide[Container.cart_service])
):
    return await service.update_item(current_user.id, item_id, request)


@router.delete("/{item_id}")
@inject
async def remove_cart_item(
    item_id:      int,
    current_user: UserResponse = Depends(get_current_user),
    service:      CartService  = Depends(Provide[Container.cart_service])
):
    await service.remove_item(current_user.id, item_id)
    return {"message": "Item removed from cart"}