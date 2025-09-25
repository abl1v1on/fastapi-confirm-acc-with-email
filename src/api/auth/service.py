import jwt
import bcrypt
from typing import Annotated
from fastapi import Depends, HTTPException, status
from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.models import User, helper
from api.users.service import UserAPIService
from .schemas import (
    PayloadSchema,
    JWTType,
    AccessTokenSchema,
    AuthCredentialsSchema,
)


class AuthAPIService:
    def __init__(self) -> None:
        self.public_key = settings.jwt.public_key
        self.private_key = settings.jwt.private_key
        self.algorithm = settings.jwt.algorithm

    async def auth_user(
        self,
        credentials: AuthCredentialsSchema,
    ) -> AccessTokenSchema:
        async with helper.session_factory() as session:
            users_service = UserAPIService(session=session)
            user = await users_service.get_user_by(
                need_raise_exception=False,
                username=credentials.username,
            )

        if not user or not self.__verify(credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid username or password",
            )

        access_token = self.create_token(user, JWTType.ACCESS)
        refresh_token = self.create_token(user, JWTType.REFRESH)
        return AccessTokenSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def encode_jwt(self, payload: PayloadSchema) -> str:
        token = jwt.encode(
            payload=payload.model_dump(),
            key=self.private_key,
            algorithm=self.algorithm,
        )
        return token

    def create_token(self, user: User, token_type: JWTType):
        payload = PayloadSchema(
            sub=str(user.id),
            email=user.email,  # type: ignore
            is_activated=user.is_activated,
            typ=token_type,
            **self.__generate_iat_and_exp(token_type),
        )
        return self.encode_jwt(payload)

    def decode_jwt(self, token: str) -> PayloadSchema:
        payload = jwt.decode(
            jwt=token,
            key=self.public_key,
            algorithms=[self.algorithm],
        )
        return PayloadSchema(**payload)

    @staticmethod
    def __verify(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode(), hashed_password=hashed_password.encode()
        )

    @staticmethod
    def __generate_iat_and_exp(token_type: JWTType) -> dict[str, datetime]:
        iat = datetime.now(timezone.utc)

        if token_type == JWTType.ACCESS:
            exp = iat + timedelta(minutes=settings.jwt.access_token_expire_minutes)
        elif token_type == JWTType.REFRESH:
            exp = iat + timedelta(days=settings.jwt.refresh_token_expire_days)
        return {"iat": iat, "exp": exp}


service_dep: type[AuthAPIService] = Annotated[
    AuthAPIService,
    Depends(AuthAPIService),
]
