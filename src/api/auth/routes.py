from typing import Annotated
from fastapi import APIRouter, Depends

from core.models import User
from .service import service_dep, email_service_dep
from .schemas import (
    AuthCredentialsSchema,
    AccessTokenSchema,
    PayloadSchema,
    ConfirmCodeSchema,
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
    user: Annotated[User, Depends(deps.user_dependency)],
    payload: Annotated[PayloadSchema, Depends(deps.payload_dependency)],
):
    return await service.refresh_token(user, payload)


@router.get("/get-activate-code", response_model=ConfirmCodeSchema)
async def handle_generate_confirm_code(
    email_service: email_service_dep,
    payload: Annotated[PayloadSchema, Depends(deps.payload_dependency)],
):
    return await email_service.send_activation_code(payload)


@router.patch("/activate", response_model=AccessTokenSchema)
async def handle_activate_user(
    service: service_dep,
    payload: Annotated[PayloadSchema, Depends(deps.payload_dependency)],
):
    return await service.activate_user(payload)
