import logging.config

import fastapi
import uvicorn
from starlette import requests, templating
from starlette.middleware import sessions

from domuwa import config
from domuwa.routers import (
    answers_router,
    game_rooms_router,
    players_router,
    questions_router,
)
from domuwa.utils import get_computer_ip
from domuwa.utils import logging as app_logging

logger = app_logging.get_logger("fastapi")
# logging.getLogger("multipart.multipart").setLevel(logging.INFO)
logging.getLogger("asyncio").setLevel(logging.INFO)

app = fastapi.FastAPI(debug=True)

app.include_router(answers_router.router)
app.include_router(game_rooms_router.router)
app.include_router(players_router.router)
app.include_router(questions_router.router)

app.add_middleware(sessions.SessionMiddleware, secret_key="guccitrip")

templates = templating.Jinja2Templates(directory="resources/templates")


@app.get("/")
async def get_home(request: requests.Request) -> templating._TemplateResponse:
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


if __name__ == "__main__":
    port = config.PORT
    address = get_computer_ip.get_ip_address(port)
    # noinspection SpellCheckingInspection,HttpUrlsUsage
    print(
        "Serwer uruchomiony. Żeby dołączyć do gry, połącz się do tej samej sieci WiFi, "
        "do której jest podłączony komputer.\n"
        "Teraz niech każdy na swoim telefonie wpisze w przeglądarkę adres "
        f"http://{address}:{port}",
    )
    uvicorn.run(app, host=address, port=port)
