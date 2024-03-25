from contextlib import asynccontextmanager

from config import settings
from domuwa import logging
from domuwa.database import create_db_and_tables
from domuwa.routers import (
    # answers_router,
    # questions_router,
    # game_rooms_router,
    players_router,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response

logger = logging.get_logger("fastapi")


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(debug=True, lifespan=lifespan)

API_PREFIX = "/api"
# app.include_router(answers_router, prefix=API_PREFIX)
# app.include_router(game_rooms_router, prefix=API_PREFIX)
app.include_router(players_router, prefix=API_PREFIX)
# app.include_router(questions_router, prefix=API_PREFIX)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_MIDDLEWARE_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_home():
    return Response("Server is running...")
