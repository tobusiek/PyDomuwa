import domuwa.answer.schema as answer_schema
import domuwa.game_room.schema as game_schema
import domuwa.player.schema as player_schema
import domuwa.question.schema as question_schema


def rebuild_schemas() -> None:
    answer_schema.AnswerBase.model_rebuild()
    answer_schema.AnswerCreate.model_rebuild()
    answer_schema.AnswerView.model_rebuild()

    player_schema.PlayerBase.model_rebuild()
    player_schema.PlayerCreate.model_rebuild()
    player_schema.PlayerView.model_rebuild()

    game_schema.GameRoomBase.model_rebuild()
    game_schema.GameRoomCreate.model_rebuild()
    game_schema.GameRoomView.model_rebuild()
    game_schema.GameRoomViewWithPlayers.model_rebuild()

    player_schema.PlayerViewWithGame.model_rebuild()

    question_schema.QuestionBase.model_rebuild()
    question_schema.QuestionCreate.model_rebuild()
    question_schema.QuestionView.model_rebuild()

    answer_schema.AnswerViewWithQuestion.model_rebuild()
