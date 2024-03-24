from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from config import settings
from domuwa.database import create_db_and_tables
from domuwa.routers import (
    answers_router,
    game_rooms_router,
    players_router,
    questions_router,
)
from domuwa.utils import logging as app_logging
from domuwa.utils.get_computer_ip import get_computer_ip
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

logger = app_logging.get_logger("fastapi")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    address = get_computer_ip(settings.API_PORT)
    print(
        "Serwer uruchomiony. Żeby dołączyć do gry, połącz się do tej samej sieci WiFi, "
        "do której jest podłączony komputer.\n"
        "Teraz niech każdy na swoim telefonie wpisze w przeglądarkę adres "
        f"http://{address}:{settings.API_PORT}",
    )
    create_db_and_tables()
    logger.critical("fix .env support for docker compose")
    yield


app = FastAPI(debug=True, lifespan=lifespan)

API_PREFIX = "/api"
# app.include_router(answers_router.router, prefix=API_PREFIX)
# app.include_router(game_rooms_router.router, prefix=API_PREFIX)
app.include_router(players_router.router, prefix=API_PREFIX)
# app.include_router(questions_router.router, prefix=API_PREFIX)

app.add_middleware(SessionMiddleware, secret_key="guccitrip")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def check_health(_: Request) -> JSONResponse:
    return JSONResponse({"ping": "pong"})
