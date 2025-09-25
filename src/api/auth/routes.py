from typing import Annotated
from fastapi import APIRouter, Depends

from .service import service_dep
from .schemas import (
    AuthCredentialsSchema,
    AccessTokenSchema,
    PayloadSchema,
)
from . import dependencies as deps


router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/login", response_model=AccessTokenSchema)
async def handle_login_user(
    service: service_dep,
    credentials: AuthCredentialsSchema,
):
    return await service.auth_user(credentials=credentials)


@router.get("/refresh", response_model=AccessTokenSchema)
async def handle_refresh_access_token(
    service: service_dep,
    payload: Annotated[PayloadSchema, Depends(deps.payload_dependency)],
):
    return await service.refresh_token(payload)
