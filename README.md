# PyDomuwa

## Domuwa is a locally hosted service, created to play games on a party

In future, there will be implementation of games like Ego or Who's most likely,
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

- [x] add tests for question
    - [ ] add tests for update and delete
- [ ] add ep for question view
- [ ] fix answer services - update and delete
- [ ] on `get_all` in questions and answers filter for `deleted` and order by `excluded`
- [ ] remove `next_version` from questions and answers
- [ ] update tests for answers
- [ ] add game type services
- [ ] add game type eps
- [ ] add game type tests
- [ ] add game category services
- [ ] add game category eps
- [ ] add game category tests
- [ ] add game room services
- [ ] add game room eps
- [ ] add game room tests
- [ ] add ranking services
- [ ] add ranking eps
- [ ] add rankihg tests

##### TODO later

- [ ] add alembic
- [ ] start ui
- [ ] add auth services
- [ ] add auth aps
- [ ] add auth eps
- [ ] add pagination
- [ ] move to postgres

