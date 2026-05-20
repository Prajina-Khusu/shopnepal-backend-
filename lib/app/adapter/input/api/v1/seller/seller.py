from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from dependency_injector.wiring import Provide, inject
from lib.app.container import Container
from lib.app.application.services.seller_service import SellerService
from lib.app.domain.dtos.seller_dto import (
    SellerApplicationRequest,
    SellerApplicationResponse,
    ReviewApplicationRequest
)
from lib.app.adapter.input.api.v1.dependencies.auth import (
    get_current_user, get_current_admin
)
from lib.app.domain.dtos.auth_dto import UserResponse

router = APIRouter(prefix="/seller", tags=["Seller"])


@router.post("/apply", response_model=SellerApplicationResponse, status_code=201)
@inject
async def apply_as_seller(
    request:      SellerApplicationRequest,
    current_user: UserResponse  = Depends(get_current_user),
    service:      SellerService = Depends(Provide[Container.seller_service])
):
    """Any logged-in user can apply to become a seller"""
    return await service.apply(current_user.id, request)


@router.get("/my-application", response_model=SellerApplicationResponse)
@inject
async def get_my_application(
    current_user: UserResponse  = Depends(get_current_user),
    service:      SellerService = Depends(Provide[Container.seller_service])
):
    """Check your own application status"""
    return await service.get_my_application(current_user.id)


@router.get("/applications", response_model=List[SellerApplicationResponse])
@inject
async def get_all_applications(
    status:       Optional[str] = Query(None),
    current_user: UserResponse  = Depends(get_current_admin),
    service:      SellerService = Depends(Provide[Container.seller_service])
):
    """Admin only — view all seller applications"""
    return await service.get_all_applications(status)


@router.patch("/applications/{application_id}/review",
              response_model=SellerApplicationResponse)
@inject
async def review_application(
    application_id: int,
    request:        ReviewApplicationRequest,
    current_user:   UserResponse  = Depends(get_current_admin),
    service:        SellerService = Depends(Provide[Container.seller_service])
):
    """Admin only — approve or reject seller application"""
    return await service.review_application(
        application_id,
        current_user.id,
        request
    )