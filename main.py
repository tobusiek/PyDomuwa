import logging.config
import os

import uvicorn
from fastapi import FastAPI, Form, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import _TemplateResponse

from db import schemas, crud
from db.models.game import Game
from db.models.player import Player
from db.models.question import Question
from games.ego import EgoGame
from utils.get_computer_ip import get_ip_address

logging.config.fileConfig(os.path.join(os.getcwd(), "resources", "logging.ini"), disable_existing_loggers=False)
logger = logging.getLogger("fastapi")
logging.getLogger("multipart.multipart").setLevel(logging.INFO)

app = FastAPI(debug=True)
app.add_middleware(SessionMiddleware, secret_key="guccitrip")
templates = Jinja2Templates(directory="resources/templates")


@app.get("/")
async def get_home(request: Request) -> _TemplateResponse:
    context = {"request": request,
               "active_games": crud.get_active_games()}
    return templates.TemplateResponse("index.html", context)


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
async def create_game(
        request: Request,
        game_name: str = Form(...),
        game_category: str = Form(...),
        game_rounds: int = Form(...)
) -> _TemplateResponse:
    logger.debug(f"{game_name=} {game_category=}")
    db_game = crud.create_game(game_name, game_category, game_rounds)
    context = {"request": request,
               "active_games": crud.get_active_games()}
    return templates.TemplateResponse("active-games.html", context)


@app.post("/games/join_game/{game_id}")
async def join_game(request: Request, game_id: int):
    nickname = request.session.get("nickname")
    logger.debug(f"{nickname=}")
    if not nickname:
        raise HTTPException(status_code=420, detail="Proszę wpisać nick, debilu")

    game = crud.get_game_by_id(game_id)
    logger.debug(f"{game=}")
    if not game:
        raise HTTPException(status_code=420, detail="Ta gra nie istnieje")

    player = crud.get_player_by_nickname(nickname)
    logger.debug(f"{player=}")
    if not player:
        player = crud.create_player(nickname)
        logger.debug(f"{player=}")

    player.set_game_id(game_id)

    context = {"request": request,
               "game": game,
               "game_players": Player.get_by_game_id(game_id)}
    return templates.TemplateResponse("game-room.html", context=context)


@app.post("/games/start_game/{game_id}")
async def start_game(game_id: int):
    db_game = Game.get_by_id(game_id)
    if not db_game:
        raise HTTPException(status_code=420, detail="Ta gra nie istnieje")
    if db_game.name == "ego":
        game = EgoGame(db_game.category)
    elif db_game.name == "whos-most-likely":
        # game = WhosMostLikelyGame()
        raise HTTPException(status_code=420, detail="Ta gra nie działa")
    game.start()


@app.post("/questions")
async def get_questions_for_game(request: Request, game_to_edit: str = Form(...)):
    questions = Question.get_by_game_type(game_to_edit, "MIXED")
    questions.append(Question("ego", "mixed", "text", 1, 0))
    context = {"request": request,
               "game_questions": questions}
    return templates.TemplateResponse("update-questions.html", context=context)


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
    print("Serwer uruchomiony. Żeby dołączyć do gry, połącz się do tej samej sieci WiFi, "
          "do której jest podłączony komputer.\n "
          "Teraz niech każdy na swoim telefonie wpisze w przeglądarkę adres "
          f"{get_ip_address(port)}:{port}")
    crud.initialize_tables()
    crud.create_constraints()
    uvicorn.run(app, host=address, port=port)
