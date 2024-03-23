from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from starlette.middleware.sessions import SessionMiddleware

from config import settings
from domuwa.routers import (
    answers_router,
    game_rooms_router,
    players_router,
    questions_router,
)
from domuwa.utils import get_computer_ip
from domuwa.utils import logging as app_logging

logger = app_logging.get_logger("fastapi")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    address = get_computer_ip.get_ip_address(settings.API_PORT)
    print(
        "Serwer uruchomiony. Żeby dołączyć do gry, połącz się do tej samej sieci WiFi, "
        "do której jest podłączony komputer.\n"
        "Teraz niech każdy na swoim telefonie wpisze w przeglądarkę adres "
        f"http://{address}:{settings.API_PORT}",
    )
    yield


app = FastAPI(debug=True, lifespan=lifespan)

API_PREFIX = "/api"
app.include_router(answers_router.router, prefix=API_PREFIX)
app.include_router(game_rooms_router.router, prefix=API_PREFIX)
app.include_router(players_router.router, prefix=API_PREFIX)
app.include_router(questions_router.router, prefix=API_PREFIX)

app.add_middleware(SessionMiddleware, secret_key="guccitrip")


@app.get("/ping")
def get_home(_: Request) -> Response:
    return Response({"ping": "pong"})
