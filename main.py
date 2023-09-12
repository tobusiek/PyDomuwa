import logging.config
import os

import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.templating import _TemplateResponse

import config
from domuwa.answer.router import router as answer_router
from domuwa.database import init_db
from domuwa.game_room.router import router as game_router
from domuwa.player.router import router as player_router
from domuwa.question.router import router as question_router
from domuwa.ranking.router import router as ranking_router
from domuwa.utils.get_computer_ip import get_ip_address

# rebuild_schemas()

logging.config.fileConfig(os.path.join(os.getcwd(), "resources", "logging.ini"), disable_existing_loggers=False)
logger = logging.getLogger("fastapi")
logging.getLogger("multipart.multipart").setLevel(logging.INFO)
logging.getLogger("asyncio").setLevel(logging.INFO)

app = FastAPI(debug=True)

app.include_router(player_router)
app.include_router(question_router)
app.include_router(answer_router)
app.include_router(game_router)
app.include_router(ranking_router)

app.add_middleware(SessionMiddleware, secret_key="guccitrip")

templates = Jinja2Templates(directory="resources/templates")


@app.get("/")
async def get_home(request: Request) -> _TemplateResponse:
    context = {"request": request, }
    return templates.TemplateResponse("index.html", context)


if __name__ == "__main__":
    address = config.HOST_ADDR
    port = config.PORT
    print("Serwer uruchomiony. Żeby dołączyć do gry, połącz się do tej samej sieci WiFi, "
          "do której jest podłączony komputer.\n"
          "Teraz niech każdy na swoim telefonie wpisze w przeglądarkę adres "
          f"{get_ip_address(port)}:{port}")
    init_db()
    uvicorn.run(app, host=address, port=port)
