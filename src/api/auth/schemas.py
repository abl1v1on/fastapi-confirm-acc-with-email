from enum import Enum
from typing import Annotated
from annotated_types import Len
from datetime import datetime
from pydantic import BaseModel, EmailStr


class JWTType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class AuthCredentialsSchema(BaseModel):
    username: Annotated[str, Len(min_length=3, max_length=60)]
    password: Annotated[str, Len(min_length=8, max_length=50)]


class PayloadSchema(BaseModel):
    sub: str
    email: EmailStr
    is_activated: bool
    iat: datetime
    exp: datetime
    typ: JWTType


class AccessTokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    typ: str = "Bearer"
