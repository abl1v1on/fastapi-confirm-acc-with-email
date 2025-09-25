from enum import Enum
from typing import Annotated
from pydantic.validators import str_validator
from pydantic_core import PydanticCustomError
from annotated_types import Len
from pydantic import BaseModel, EmailStr


class JWTType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class NumericStr(str):
    @classmethod
    def __get_pydantic_validators__(cls):
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: str) -> str:
        if not value.isdigit():
            raise PydanticCustomError(
                "numeric_str",
                "value must be a string of numbers",
            )
        return value


class AuthCredentialsSchema(BaseModel):
    username: Annotated[str, Len(min_length=3, max_length=60)]
    password: Annotated[str, Len(min_length=8, max_length=50)]


class PayloadSchema(BaseModel):
    sub: NumericStr
    email: EmailStr
    is_activated: bool
    typ: JWTType


class AccessTokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    typ: str = "Bearer"
