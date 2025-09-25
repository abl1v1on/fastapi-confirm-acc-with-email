import uvicorn
from fastapi import FastAPI

from core import settings
from api import main_api_router


app = FastAPI()
app.include_router(main_api_router)


if __name__ == "__main__":
    uvicorn.run(**settings.server.model_dump())
