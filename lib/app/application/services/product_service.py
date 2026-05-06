import re
from fastapi import HTTPException, status
from lib.app.domain.services.base import ProductServiceBase
from lib.app.domain.repositories import ProductRepository
from lib.app.domain.dtos.product_dto import (
    ProductListRequest, ProductListResponse,
    ProductResponse, CreateProductRequest, UpdateProductRequest
)


def slugify(text: str) -> str:
    text = text.lower().strip()
    return re.sub(r"[\s_]+", "-", re.sub(r"[^\w\s-]", "", text))


class ProductService(ProductServiceBase):

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def get_all(self, request: ProductListRequest) -> ProductListResponse:
        items = self.product_repository.get_all(
            skip        = request.skip,
            limit       = request.limit,
            search      = request.search,
            category_id = request.category_id
        )
        total = self.product_repository.count(
            search      = request.search,
            category_id = request.category_id
        )
        return ProductListResponse(
            items = [ProductResponse.model_validate(p) for p in items],
            total = total,
            skip  = request.skip,
            limit = request.limit
        )

    async def get_by_slug(self, slug: str) -> ProductResponse:
        product = self.product_repository.get_by_slug(slug)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return ProductResponse.model_validate(product)

    async def create(self, request: CreateProductRequest) -> ProductResponse:
        slug    = slugify(request.name)
        product = self.product_repository.create({
            "name":        request.name,
            "slug":        slug,
            "description": request.description,
            "price":       request.price,
            "sale_price":  request.sale_price,
            "stock":       request.stock,
            "category_id": request.category_id,
        })
        return ProductResponse.model_validate(product)

    async def update(
        self,
        product_id: int,
        request: UpdateProductRequest
    ) -> ProductResponse:
        data    = request.model_dump(exclude_none=True)
        product = self.product_repository.update(product_id, data)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return ProductResponse.model_validate(product)

    async def delete(self, product_id: int) -> bool:
        result = self.product_repository.delete(product_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return True