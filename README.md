# PyDomuwa

## Domuwa is a locally hosted service, created to play games on a party

In the future, there will be implementation of games like Ego or Who's most likely,
Cards against humanity, etc.

App uses Python 3.11, FastAPI, SQLite database (pointed to file in project directory)
with alembic. Client will be created with React + Typescript (later).

Every player needs to connect their device (phone or pc) to the same Wi-Fi
as pc that app is hosted on. Then everybody goes to http address,
which is printed in console once the app has been started.

Every player can modify question and answers database (initially empty):

- add their own
- modify existing ones
- mark questions as excluded
- delete one by one

### Run app (.env needs fix)

```console
docker compose up -d --build
```

### Shutdown app

```console
docker compose down
```

### List docker logs

```console
docker logs <container name> [-f] [-t]
```

Then go to http address printed in console

#### TODO

- [ ] fix autoformatting in pycharm using ruff (probably paths)
- [x] raise 404 in routers
- [x] add tests for question
    - [ ] understand `next_version` from questions and answers
    - [x] add tests for update and delete
- [ ] add ep for questions view
- [x] fix answer services - update and delete
- [ ] on `get_all` in questions and answers filter for `deleted` and order by `excluded`
- [x] update tests for answers
- [x] add game type
- [x] add qna category
- [x] add game category
- add auth
    - [ ] add user model
    - [ ] update player to use user
    - update allowed only by admin
        - [ ] game type
        - [ ] qna category
        - [ ] game category
    - delete allowed only by admin
        - [ ] game type
        - [ ] qna category
        - [ ] game category
    - update author on update
        - [ ] question
        - [ ] answer
- add game room
    - [ ] services
    - [ ] router
    - [ ] tests
- add ranking
    - [ ] services
    - [ ] router
    - [ ] tests

##### TODO later

- [ ] add alembic
- [ ] start ui
- [ ] add pagination
- [ ] move to postgres
- [ ] add auth with fb
