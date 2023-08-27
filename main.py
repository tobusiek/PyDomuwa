import logging.config
import os

import uvicorn
from fastapi import FastAPI, Form
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import _TemplateResponse

from db import schemas, crud
from utils.get_computer_ip import get_ip_address

logging.config.fileConfig(os.path.join(os.getcwd(), "resources", "logging.ini"), disable_existing_loggers=False)
logger = logging.getLogger("fastapi")

app = FastAPI(debug=True)
app.add_middleware(SessionMiddleware, secret_key="guccitrip")
templates = Jinja2Templates(directory="resources/templates")


@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/post_nickname")
async def post_nickname(request: Request, nickname: str = Form(None)):
    logger.debug(f"{nickname=}")
    if nickname and not request.session.get("nickname"):
        request.session["nickname"] = nickname
        player = crud.get_player_by_nickname(nickname)
        if not player:
            player = crud.create_player(nickname)
        return RedirectResponse(url=request.url.path)
    return templates.TemplateResponse("nickname.html", {"request": request})


@app.get("/get_active_games", response_model=list[schemas.Game])
async def get_active_games(request: Request) -> _TemplateResponse:
    active_games = crud.get_active_games()
    logger.debug(f"{active_games=}")
    return templates.TemplateResponse("index.html", {"request": request, "active_games": active_games})


@app.post("/games/create_game", response_model=schemas.Game)
async def create_game(request: Request, game_name: str = Form(...)) -> RedirectResponse:
    logger.debug(f"{game_name=}")
    game = schemas.GameCreate(**{"name": game_name})
    logger.debug(f"{game=}")
    context = {'request': request,
               'game': crud.create_game(game)}
    return RedirectResponse(url=request.url.path)


# @app.post("/games/join_game/{game_id}")
# async def join_game(game_id: int, request: Request):
#     nickname = request.session.get("nickname")
#     logger.debug(f"{nickname=}")
#     if not nickname:
#         raise HTTPException(status_code=420, detail="Proszę wpisać nick, debilu")
#
#     game = crud.get_game_by_id(game_id)
#     logger.debug(f"{game=}")
#     if not game:
#         raise HTTPException(status_code=420, detail="Ta gra nie istnieje")
#
#     player = crud.get_player_by_nickname(nickname)
#     logger.debug(f"{player=}")
#     if not player:
#         player = crud.create_player(schemas.PlayerCreate(name=nickname))
#
#     game.players.append(player)
#
#     return {"message": "Dołączasz do gry!"}
#
#
# @app.post("/games/add_player/{game_id}/players/", response_model=schemas.Player)
# async def add_player_to_game(game_id: int, player: schemas.PlayerCreate):
#     return crud.add_player_to_game(game_id, player)
#
#
# @app.put("/questions/{question_id}/", response_model=schemas.Question)
# async def update_question(question_id: int, question: schemas.QuestionUpdate):
#     return crud.update_question(question_id, question)
#
#
# @app.put("/answers/{answer_id}/", response_model=schemas.Answer)
# async def update_answer(answer_id: int, answer: schemas.AnswerUpdate):
#     return crud.update_answer(answer_id, answer)


if __name__ == "__main__":
    address = "0.0.0.0"
    port = 42069
    print("Serwer uruchomiony. Żeby dołączyć do gry, połącz się do tej samej sieci WiFi,"
          " do której jest podłączony komputer.")
    print(f"Teraz niech każdy na swoim telefonie wpisze w przeglądarkę adres: {get_ip_address(port)}:{port}")
    crud.initialize_tables()
    uvicorn.run(app, host=address, port=port)
