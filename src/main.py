import uvicorn
from fastapi import FastAPI

from core import settings


app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(**settings.server.model_dump())
