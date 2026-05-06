from fastapi import APIRouter, Depends
from typing import List
from dependency_injector.wiring import Provide, inject
from lib.app.container import Container
from lib.app.application.services.category_service import CategoryService
from lib.app.domain.dtos.category_dto import CategoryResponse, CreateCategoryRequest
from lib.app.adapter.input.api.v1.dependencies.auth import get_current_admin
from lib.app.domain.dtos.auth_dto import UserResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponse])
@inject
async def get_categories(
    service: CategoryService = Depends(Provide[Container.category_service])
):
    return await service.get_all()


@router.post("/", response_model=CategoryResponse, status_code=201)
@inject
async def create_category(
    request:      CreateCategoryRequest,
    service:      CategoryService = Depends(Provide[Container.category_service]),
    current_user: UserResponse    = Depends(get_current_admin)
):
    return await service.create(request)