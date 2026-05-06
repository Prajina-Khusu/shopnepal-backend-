from typing import List
from fastapi import HTTPException, status
from lib.app.domain.services.base import CategoryServiceBase
from lib.app.domain.repositories import CategoryRepository
from lib.app.domain.dtos.category_dto import CategoryResponse, CreateCategoryRequest


class CategoryService(CategoryServiceBase):

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def get_all(self) -> List[CategoryResponse]:
        categories = self.category_repository.get_all()
        return [CategoryResponse.model_validate(c) for c in categories]

    async def create(self, request: CreateCategoryRequest) -> CategoryResponse:
        existing = self.category_repository.get_by_slug(request.slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category slug already exists"
            )
        category = self.category_repository.create(request.model_dump())
        return CategoryResponse.model_validate(category)