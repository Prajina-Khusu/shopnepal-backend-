from typing import List, Optional
from fastapi import HTTPException, status
from lib.app.adapter.output.persistence.seller.repositories import SellerRepositoryImpl
from lib.app.domain.dtos.seller_dto import (
    SellerApplicationRequest,
    SellerApplicationResponse,
    ReviewApplicationRequest
)


class SellerService:

    def __init__(self, seller_repository: SellerRepositoryImpl):
        self.seller_repository = seller_repository

    async def apply(
        self,
        user_id: int,
        request: SellerApplicationRequest
    ) -> SellerApplicationResponse:
        # Check if already applied
        existing = self.seller_repository.get_by_user(user_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"You already have an application with status: {existing['status']}"
            )
        application = self.seller_repository.create(user_id, {
            "shop_name":    request.shop_name,
            "shop_address": request.shop_address,
            "phone":        request.phone,
            "description":  request.description,
        })
        return SellerApplicationResponse(**application)

    async def get_my_application(self, user_id: int) -> SellerApplicationResponse:
        application = self.seller_repository.get_by_user(user_id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No application found"
            )
        return SellerApplicationResponse(**application)

    async def get_all_applications(
        self,
        status: Optional[str] = None
    ) -> List[SellerApplicationResponse]:
        applications = self.seller_repository.get_all(status)
        return [SellerApplicationResponse(**a) for a in applications]

    async def review_application(
        self,
        application_id: int,
        admin_id:       int,
        request:        ReviewApplicationRequest
    ) -> SellerApplicationResponse:
        if request.status not in ["approved", "rejected"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status must be 'approved' or 'rejected'"
            )
        application = self.seller_repository.update_status(
            application_id,
            request.status,
            admin_id
        )
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )
        # If approved → promote user to seller
        if request.status == "approved":
            self.seller_repository.update_user_role(
                application["user_id"], "seller"
            )
        return SellerApplicationResponse(**application)