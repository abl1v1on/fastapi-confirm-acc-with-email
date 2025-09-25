from typing import Annotated
from annotated_types import Gt
from fastapi import APIRouter, status

from .schemas import (
    GetUserSchema,
    CreateUserSchema,
    UpdateUserSchema,
    PartialUpdateUserSchema,
)
from .service import service_dep


router = APIRouter(prefix="/users", tags=["Пользователи"])

int_gt_0 = Annotated[int, Gt(0)]


@router.get("/", response_model=list[GetUserSchema])
async def handle_get_users(service: service_dep):
    return await service.get_users()


@router.get("/{user_id}", response_model=GetUserSchema)
async def handle_get_user(service: service_dep, user_id: int_gt_0):
    return await service.get_user(user_id)


@router.post("/", response_model=GetUserSchema, status_code=status.HTTP_201_CREATED)
async def handle_create_user(service: service_dep, schema: CreateUserSchema):
    return await service.create_user(schema)


@router.put("/{user_id}", response_model=GetUserSchema)
async def handle_update_user(
    service: service_dep, user_id: int_gt_0, schema: UpdateUserSchema
):
    return await service.update_user(user_id=user_id, schema=schema)


@router.patch("/{user_id}", response_model=GetUserSchema)
async def handle_partial_update_user(
    service: service_dep, user_id: int_gt_0, schema: PartialUpdateUserSchema
):
    return await service.update_user(user_id=user_id, schema=schema)


@router.delete(
    "/{user_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def handle_delete_user(service: service_dep, user_id: int_gt_0):
    return await service.delete_user(user_id)
