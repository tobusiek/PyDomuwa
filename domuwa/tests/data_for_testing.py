ID = "id"
QUESTION_ID = "question_id"
GAME_NAME = "game_name"
CATEGORY = "category"
AUTHOR = "author"
TEXT = "text"
EXCLUDED = "excluded"
ANSWERS = "answers"

TEST_QUESTIONS_VALID = [
    {
        GAME_NAME: "ego",
        CATEGORY: "MIXED",
        AUTHOR: "User1",
        TEXT: "text 1",
        EXCLUDED: False,
    },
    {
        GAME_NAME: "ego",
        CATEGORY: "NSFW",
        AUTHOR: "User2",
        TEXT: "text 2",
        EXCLUDED: True,
    },
    {
        GAME_NAME: "who's most likely",
        CATEGORY: "SFW",
        AUTHOR: "User1",
        TEXT: "text 3",
        EXCLUDED: True,
    }
]

TEST_QUESTIONS_INVALID = {
    "game_name": {

    },
    "category": {

    },
    "author": {

    },
    "text": {

    },
    "excluded": {

    }
}

ANSWER_ID = "answer_id"
CORRECT = "correct"
QUESTION_ID = "question_id"
QUESTION = "question"

TEST_ANSWERS_VALID = [
    {
        AUTHOR: "User1",
        TEXT: "text 1",
    },
    {
        AUTHOR: "User1",
        TEXT: "text 2",
        CORRECT: True,
    },
    {
        AUTHOR: "User2",
        TEXT: "text 3",
        CORRECT: False,
    }
]

TEST_ANSWERS_INVALID = {
    AUTHOR: {
        AUTHOR: 1,
        TEXT: "text",
        QUESTION_ID: 1
    },
    TEXT: {
        AUTHOR: "User",
        TEXT: False,
        QUESTION_ID: 1,
    },
    CORRECT: {
        AUTHOR: "User",
        TEXT: "text",
        QUESTION_ID: 1,
        CORRECT: "null",
    },
    QUESTION_ID: {
        AUTHOR: "User",
        TEXT: "text",
        QUESTION_ID: "null",
    },
}

TEST_GAME_ROOMS_VALID = [

]

TEST_PLAYERS_VALID = [

]

TEST_RANKINGS_VALID = [

]
