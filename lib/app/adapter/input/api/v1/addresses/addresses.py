from fastapi import APIRouter, Depends
from typing import List
from dependency_injector.wiring import Provide, inject
from lib.app.container import Container
from lib.app.application.services.address_service import AddressService
from lib.app.domain.dtos.address_dto import AddressCreateRequest, AddressResponse
from lib.app.adapter.input.api.v1.dependencies.auth import get_current_user
from lib.app.domain.dtos.auth_dto import UserResponse

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/", response_model=AddressResponse, status_code=201)
@inject
async def create_address(
    request:      AddressCreateRequest,
    current_user: UserResponse   = Depends(get_current_user),
    service:      AddressService = Depends(Provide[Container.address_service])
):
    return await service.create(current_user.id, request)


@router.get("/", response_model=List[AddressResponse])
@inject
async def get_addresses(
    current_user: UserResponse   = Depends(get_current_user),
    service:      AddressService = Depends(Provide[Container.address_service])
):
    return await service.get_by_user(current_user.id)


@router.get("/{address_id}", response_model=AddressResponse)
@inject
async def get_address(
    address_id:   int,
    current_user: UserResponse   = Depends(get_current_user),
    service:      AddressService = Depends(Provide[Container.address_service])
):
    return await service.get_by_id(current_user.id, address_id)