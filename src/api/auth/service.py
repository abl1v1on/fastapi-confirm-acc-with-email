import bcrypt
import jwt
from fastapi import Depends
from typing import Annotated

from core import settings
from .schemas import PayloadSchema, AccessTokenSchema


class AuthAPIService:
    def __init__(self) -> None:
        self.public_key = settings.jwt.public_key
        self.private_key = settings.jwt.private_key
        self.algorithm = settings.jwt.algorithm

    def encode_jwt(self, payload: PayloadSchema) -> str:
        token = jwt.encode(
            payload=payload.model_dump(),
            key=self.private_key,
            algorithm=self.algorithm,
        )
        return token

    def decode_jwt(self, token: str) -> PayloadSchema:
        payload = jwt.decode(
            jwt=token,
            key=self.public_key,
            algorithms=[self.algorithm],
        )
        return PayloadSchema(**payload)

    @staticmethod
    def verify(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode(), hashed_password=hashed_password.encode()
        )


service_dep: type[AuthAPIService] = Annotated[AuthAPIService, Depends(AuthAPIService)]
