from fastapi import APIRouter, Depends, Query
from typing import Optional
from dependency_injector.wiring import Provide, inject
from lib.app.container import Container
from lib.app.application.services.product_service import ProductService
from lib.app.domain.dtos.product_dto import (
    ProductListResponse, ProductResponse,
    CreateProductRequest, UpdateProductRequest,
    ProductListRequest
)
from lib.app.adapter.input.api.v1.dependencies.auth import get_current_seller
from lib.app.domain.dtos.auth_dto import UserResponse

router = APIRouter(prefix="/seller/products", tags=["Seller Products"])


@router.get("/", response_model=ProductListResponse)
@inject
async def get_my_products(
    skip:         int            = Query(0,  ge=0),
    limit:        int            = Query(20, ge=1, le=100),
    search:       Optional[str]  = Query(None),
    current_user: UserResponse   = Depends(get_current_seller),
    service:      ProductService = Depends(Provide[Container.product_service])
):
    return await service.get_all(ProductListRequest(
        skip      = skip,
        limit     = limit,
        search    = search,
        seller_id = current_user.id,
    ))


@router.post("/", response_model=ProductResponse, status_code=201)
@inject
async def create_my_product(
    request:      CreateProductRequest,
    current_user: UserResponse   = Depends(get_current_seller),
    service:      ProductService = Depends(Provide[Container.product_service])
):
    return await service.create(request, seller_id=current_user.id)


@router.put("/{product_id}", response_model=ProductResponse)
@inject
async def update_my_product(
    product_id:   int,
    request:      UpdateProductRequest,
    current_user: UserResponse   = Depends(get_current_seller),
    service:      ProductService = Depends(Provide[Container.product_service])
):
    return await service.update(product_id, request, seller_id=current_user.id)


@router.delete("/{product_id}")
@inject
async def delete_my_product(
    product_id:   int,
    current_user: UserResponse   = Depends(get_current_seller),
    service:      ProductService = Depends(Provide[Container.product_service])
):
    await service.delete(product_id, seller_id=current_user.id)
    return {"message": "Product deleted"}