from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dependency_injector.wiring import Provide, inject
from lib.app.container import Container
from lib.app.application.services.auth_service import AuthService
from lib.app.domain.dtos.auth_dto import UserResponse

security = HTTPBearer()


@inject
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service:     AuthService = Depends(Provide[Container.auth_service])
) -> UserResponse:
    return await service.get_current_user(credentials.credentials)


async def get_current_admin(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def get_current_seller(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    if current_user.role not in ["seller", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seller access required"
        )
    return current_user