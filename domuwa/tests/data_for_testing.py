ID = "id"
AUTHOR = "author"
TEXT = "text"
QUESTION_ID = "question_id"
CORRECT = "correct"

TEST_ANSWERS_VALID = [
    {
        AUTHOR: "User1",
        TEXT: "text 1",
        QUESTION_ID: "1"
    },
    {
        AUTHOR: "User1",
        TEXT: "text 2",
        QUESTION_ID: 2,
        CORRECT: True,
    },
    {
        AUTHOR: "User2",
        TEXT: "text 3",
        QUESTION_ID: 2,
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

TEST_QUESTIONS_VALID = [
    {""}
]

TEST_RANKINGS_VALID = [

]
