import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db import crud, schemas
from db.database import get_db

app = FastAPI()


@app.get('/')
def home() -> str:
    return "Elo, gucci trip"


@app.post("/games/", response_model=schemas.Game)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    return crud.create_game(db, game)


@app.post("/games/{game_id}/players/", response_model=schemas.Player)
def add_player_to_game(game_id: int, player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return crud.add_player_to_game(db, game_id, player)


@app.put("/questions/{question_id}/", response_model=schemas.Question)
def update_question(question_id: int, question: schemas.QuestionUpdate, db: Session = Depends(get_db)):
    return crud.update_question(db, question_id, question)


@app.put("/answers/{answer_id}/", response_model=schemas.Answer)
def update_answer(answer_id: int, answer: schemas.AnswerUpdate, db: Session = Depends(get_db)):
    return crud.update_answer(db, answer_id, answer)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=42069)
