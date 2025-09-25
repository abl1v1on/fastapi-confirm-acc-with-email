from fastapi import APIRouter

from .service import service_dep
from .schemas import (
    AuthCredentialsSchema,
    AccessTokenSchema,
)


router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/login", response_model=AccessTokenSchema)
async def handle_login_user(
    service: service_dep,
    credentials: AuthCredentialsSchema,
):
    return await service.auth_user(credentials=credentials)
