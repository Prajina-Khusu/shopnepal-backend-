from typing import List
from fastapi import HTTPException, status
from lib.app.domain.repositories import AddressRepository
from lib.app.domain.dtos.address_dto import AddressCreateRequest, AddressResponse


class AddressService:

    def __init__(self, address_repository: AddressRepository):
        self.address_repository = address_repository

    async def create(self, user_id: int, request: AddressCreateRequest) -> AddressResponse:
        address = self.address_repository.create(user_id, request.model_dump())
        return AddressResponse(**address)

    async def get_by_user(self, user_id: int) -> List[AddressResponse]:
        addresses = self.address_repository.get_by_user(user_id)
        return [AddressResponse(**a) for a in addresses]

    async def get_by_id(self, user_id: int, address_id: int) -> AddressResponse:
        address = self.address_repository.get_by_id(address_id)
        if not address:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
        if address["user_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your address")
        return AddressResponse(**address)