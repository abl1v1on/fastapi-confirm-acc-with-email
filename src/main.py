import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core import settings
from api import main_api_router


app = FastAPI()
app.include_router(main_api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(**settings.server.model_dump())
