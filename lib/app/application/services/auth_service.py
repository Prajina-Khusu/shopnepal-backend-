from fastapi import HTTPException, status
from lib.app.domain.services.base import AuthServiceBase
from lib.app.domain.repositories import UserRepository
from lib.app.domain.dtos.auth_dto import (
    RegisterRequest, LoginRequest,
    TokenResponse, UserResponse
)
from lib.core.utils.security import (
    hash_password, verify_password, create_access_token
)


class AuthService(AuthServiceBase):

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, request: RegisterRequest) -> UserResponse:
        existing = self.user_repository.get_by_email(request.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        user = self.user_repository.create({
            "name":     request.name,
            "email":    request.email,
            "password": hash_password(request.password),
            "phone":    request.phone,
            "role":     "customer"
        })
        return UserResponse(**user)

    async def login(self, request: LoginRequest) -> TokenResponse:
        user = self.user_repository.get_by_email(request.email)
        if not user or not verify_password(request.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        token = create_access_token({
            "sub":  str(user["id"]),
            "role": user["role"]
        })
        return TokenResponse(access_token=token)

    async def get_current_user(self, token: str) -> UserResponse:
        from lib.core.utils.security import decode_access_token
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        user = self.user_repository.get_by_id(int(payload["sub"]))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse(**user)