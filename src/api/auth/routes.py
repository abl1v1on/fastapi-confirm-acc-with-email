from fastapi import APIRouter, HTTPException, status

from .service import service_dep
from .schemas import (
    AuthCredentialsSchema,
    AccessTokenSchema,
    PayloadSchema,
    JWTType,
)
from api.users.service import service_dep as users_service_dep


router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/login", response_model=AccessTokenSchema)
async def handle_login_user(
    auth_service: service_dep,
    users_service: users_service_dep,
    credentials: AuthCredentialsSchema,
):
    user = await users_service.get_user_by(
        need_raise_exception=False,
        username=credentials.username,
    )

    if not user or not auth_service.verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )

    access_token_payload = PayloadSchema(
        sub=str(user.id),  # type: ignore
        email=user.email,  # type: ignore
        is_activated=user.is_activated,
        typ=JWTType.ACCESS,
    )
    access_token = auth_service.encode_jwt(access_token_payload)

    refresh_token_payload = PayloadSchema(
        sub=str(user.id),  # type: ignore
        email=user.email,  # type: ignore
        is_activated=user.is_activated,
        typ=JWTType.REFRESH,
    )
    refresh_token = auth_service.encode_jwt(refresh_token_payload)

    return AccessTokenSchema(access_token=access_token, refresh_token=refresh_token)
