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
from lib.app.adapter.input.api.v1.dependencies.auth import (
    get_current_user, get_current_admin
)
from lib.app.domain.dtos.auth_dto import UserResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=ProductListResponse)
@inject
async def get_products(
    skip:        int           = Query(0,    ge=0),
    limit:       int           = Query(20,   ge=1, le=100),
    search:      Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    service:     ProductService = Depends(Provide[Container.product_service])
):
    return await service.get_all(ProductListRequest(
        skip=skip, limit=limit,
        search=search, category_id=category_id
    ))


@router.get("/{slug}", response_model=ProductResponse)
@inject
async def get_product(
    slug:    str,
    service: ProductService = Depends(Provide[Container.product_service])
):
    return await service.get_by_slug(slug)


@router.post("/", response_model=ProductResponse, status_code=201)
@inject
async def create_product(
    request:      CreateProductRequest,
    service:      ProductService = Depends(Provide[Container.product_service]),
    current_user: UserResponse   = Depends(get_current_admin)
):
    return await service.create(request)


@router.put("/{product_id}", response_model=ProductResponse)
@inject
async def update_product(
    product_id:   int,
    request:      UpdateProductRequest,
    service:      ProductService = Depends(Provide[Container.product_service]),
    current_user: UserResponse   = Depends(get_current_admin)
):
    return await service.update(product_id, request)


@router.delete("/{product_id}")
@inject
async def delete_product(
    product_id:   int,
    service:      ProductService = Depends(Provide[Container.product_service]),
    current_user: UserResponse   = Depends(get_current_admin)
):
    await service.delete(product_id)
    return {"message": "Product deleted successfully"}