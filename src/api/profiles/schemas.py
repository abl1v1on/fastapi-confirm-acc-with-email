from typing import Annotated
from annotated_types import Len, Gt
from pydantic import BaseModel


class BaseProfileSchema(BaseModel):
    first_name: Annotated[str | None, Len(min_length=1, max_length=60)] = None
    last_name: Annotated[str | None, Len(min_length=1, max_length=60)] = None
    bio: Annotated[str | None, Len(min_length=1, max_length=200)] = None


class GetProfileSchema(BaseProfileSchema):
    id: Annotated[int, Gt(0)]
    user_id: Annotated[int, Gt(0)]


class GetProfileWithoutUserSchema(BaseProfileSchema):
    pass
