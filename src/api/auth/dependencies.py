from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.models import User
from api.users.service import service_dep as users_service_dep
from .exc import InvalidTokenTypeException
from .schemas import PayloadSchema, JWTType
from .service import service_dep


http_bearer = HTTPBearer()


def token_dependency(
    auth_headers: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> str:
    token = auth_headers.credentials
    return token


def payload_dependency(
    service: service_dep,
    token: Annotated[str, Depends(token_dependency)],
) -> PayloadSchema:
    payload = service.decode_jwt(token)
    return payload


async def user_dependency(
    users_service: users_service_dep,
    payload: Annotated[PayloadSchema, Depends(payload_dependency)],
) -> User:
    if payload.typ != JWTType.ACCESS:
        raise InvalidTokenTypeException()

    user_id = int(payload.sub)
    return await users_service.get_user_by_id(user_id)
