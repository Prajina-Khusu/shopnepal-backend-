from fastapi import APIRouter, Depends
from typing import List
from dependency_injector.wiring import Provide, inject
from lib.app.container import Container
from lib.app.application.services.review_service import ReviewService
from lib.app.domain.dtos.review_dto import ReviewResponse, CreateReviewRequest
from lib.app.adapter.input.api.v1.dependencies.auth import get_current_user
from lib.app.domain.dtos.auth_dto import UserResponse

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/{product_id}", response_model=List[ReviewResponse])
@inject
async def get_reviews(
    product_id: int,
    service:    ReviewService = Depends(Provide[Container.review_service])
):
    return await service.get_reviews(product_id)


@router.post("/{product_id}", response_model=ReviewResponse, status_code=201)
@inject
async def create_review(
    product_id:   int,
    request:      CreateReviewRequest,
    current_user: UserResponse  = Depends(get_current_user),
    service:      ReviewService = Depends(Provide[Container.review_service])
):
    return await service.create(current_user.id, product_id, request)