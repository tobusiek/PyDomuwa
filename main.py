import logging.config
import os

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import _TemplateResponse

from db import crud, schemas
from db.database import get_db

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
    if nickname:
        request.session["nickname"] = nickname
        return RedirectResponse(url=request.url.path)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/get_active_games", response_model=list[schemas.Game])
async def get_active_games(request: Request, db: Session = Depends(get_db)) -> _TemplateResponse:
    active_games = crud.get_active_games(db)
    logger.debug(f"{active_games=}")
    return templates.TemplateResponse("index.html", {"request": request, "active_games": active_games})


@app.post("/games/create_game", response_model=schemas.Game)
async def create_game(game_name: str = Form(...), db: Session = Depends(get_db)) -> schemas.Game:
    logger.debug(f"{game_name=}")
    game = schemas.GameCreate(**{"name": game_name})
    logger.debug(f"{game=}")
    return crud.create_game(db, game)


@app.post("/games/join_game/{game_id}")
async def join_game(game_id: int, request: Request, db: Session = Depends(get_db)):
    nickname = request.session.get("nickname")
    logger.debug(f"{nickname=}")
    if not nickname:
        raise HTTPException(status_code=420, detail="Proszę wpisać nick, debilu")

    game = crud.get_game_by_id(db, game_id)
    logger.debug(f"{game=}")
    if not game:
        raise HTTPException(status_code=420, detail="Ta gra nie istnieje")

    player = crud.get_player_by_nickname(db, nickname)
    logger.debug(f"{player=}")
    if not player:
        player = crud.create_player(db, schemas.PlayerCreate(name=nickname))

    game.players.append(player)
    db.commit()

    return {"message": "Dołączasz do gry!"}


@app.post("/games/add_player/{game_id}/players/", response_model=schemas.Player)
async def add_player_to_game(game_id: int, player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return crud.add_player_to_game(db, game_id, player)


@app.put("/questions/{question_id}/", response_model=schemas.Question)
async def update_question(question_id: int, question: schemas.QuestionUpdate, db: Session = Depends(get_db)):
    return crud.update_question(db, question_id, question)


@app.put("/answers/{answer_id}/", response_model=schemas.Answer)
async def update_answer(answer_id: int, answer: schemas.AnswerUpdate, db: Session = Depends(get_db)):
    return crud.update_answer(db, answer_id, answer)


if __name__ == "__main__":
    address = "0.0.0.0"
    port = 42069
    uvicorn.run(app, host=address, port=port)
