from fastapi import APIRouter

from .users import users_router
from .auth import auth_router


main_api_router = APIRouter(prefix="/api")
main_api_router.include_router(users_router)
main_api_router.include_router(auth_router)
