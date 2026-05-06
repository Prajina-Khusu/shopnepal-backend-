from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from lib.app.container import Container
from lib.app.application.services.auth_service import AuthService
from lib.app.domain.dtos.auth_dto import (
    RegisterRequest, LoginRequest,
    TokenResponse, UserResponse
)
from lib.app.adapter.input.api.v1.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
@inject
async def register(
    request: RegisterRequest,
    service: AuthService = Depends(Provide[Container.auth_service])
):
    return await service.register(request)


@router.post("/login", response_model=TokenResponse)
@inject
async def login(
    request: LoginRequest,
    service: AuthService = Depends(Provide[Container.auth_service])
):
    return await service.login(request)


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: UserResponse = Depends(get_current_user)
):
    return current_user