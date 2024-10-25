from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import initialize_db
from app.models import *
from app.routes import champion
from app.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(champion.router)
