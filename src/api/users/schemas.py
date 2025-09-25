from datetime import datetime
from typing import Annotated
from annotated_types import Len, Gt
from pydantic import BaseModel, EmailStr, field_validator


class BaseUserSchema(BaseModel):
    username: Annotated[str, Len(min_length=3, max_length=60)]
    email: EmailStr


class GetUserSchema(BaseUserSchema):
    id: Annotated[int, Gt(0)]
    created_at: datetime


class CreateUserSchema(BaseUserSchema):
    password: Annotated[str, Len(min_length=8, max_length=50)]


class UpdateUserSchema(CreateUserSchema):
    pass


class PartialUpdateUserSchema(BaseModel):
    username: Annotated[str | None, Len(min_length=3, max_length=60)] = None
    email: EmailStr | None = None
    password: Annotated[str | None, Len(min_length=8, max_length=50)] = None
