import logging.config
import os

import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.templating import _TemplateResponse

from domuwa import config
from domuwa.routers.answers_router import router as answer_router
from domuwa.routers.game_rooms_router import router as game_router
from domuwa.routers.players_router import router as player_router
from domuwa.routers.questions_router import router as question_router
from domuwa.utils.get_computer_ip import get_ip_address

logging.config.fileConfig(os.path.join(os.getcwd(), "resources", "logging.ini"), disable_existing_loggers=False)
logger = logging.getLogger("fastapi")
logging.getLogger("multipart.multipart").setLevel(logging.INFO)
logging.getLogger("asyncio").setLevel(logging.INFO)

app = FastAPI(debug=True)

app.include_router(answer_router)
app.include_router(game_router)
app.include_router(player_router)
app.include_router(question_router)

app.add_middleware(SessionMiddleware, secret_key="guccitrip")

templates = Jinja2Templates(directory="resources/templates")


@app.get("/")
async def get_home(request: Request) -> _TemplateResponse:
    context = {"request": request }
    return templates.TemplateResponse("index.html", context)


if __name__ == "__main__":
    port = config.PORT
    address = get_ip_address(port)
    print("Serwer uruchomiony. Żeby dołączyć do gry, połącz się do tej samej sieci WiFi, "
          "do której jest podłączony komputer.\n"
          "Teraz niech każdy na swoim telefonie wpisze w przeglądarkę adres "
          f"http://{address}:{port}")
    uvicorn.run(app, host=address, port=port)
