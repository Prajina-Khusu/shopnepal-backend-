from typing import List
from fastapi import HTTPException, status
from lib.app.domain.services.base import ReviewServiceBase
from lib.app.domain.repositories import ReviewRepository
from lib.app.domain.dtos.review_dto import ReviewResponse, CreateReviewRequest


class ReviewService(ReviewServiceBase):

    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    async def get_reviews(self, product_id: int) -> List[ReviewResponse]:
        reviews = self.review_repository.get_by_product(product_id)
        return [ReviewResponse.model_validate(r) for r in reviews]

    async def create(
        self,
        user_id: int,
        product_id: int,
        request: CreateReviewRequest
    ) -> ReviewResponse:
        existing = self.review_repository.get_by_user_and_product(
            user_id, product_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already reviewed this product"
            )
        review = self.review_repository.create(
            user_id    = user_id,
            product_id = product_id,
            rating     = request.rating,
            comment    = request.comment or ""
        )
        return ReviewResponse.model_validate(review)