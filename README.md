# PyDomuwa

## Domuwa is a locally hosted service, created to play games like Ego or Who's most likely with friends on a party.

App uses Python 3.10, FastAPI, SQLite database (pointed to file in project directory) with alembic.
Pages were created with HTMX and Tailwind - JS usage limited to minimum (BIG W, js sucks ass).

Every player needs to connect their device (phone or pc) to the same Wi-Fi as pc that app is hosted on.
Then everybody goes to http address, which is printed in console once the app has been started. <br>

Every player can modify question and answers database (initially empty):

- add their own
- modify existing ones
- mark questions as excluded
- delete one by one

### Initialize virtual environment

```console
python - m venv
source venv / bin / activate
pip install - r requirements.txt
```

### Initialize alembic

```console
alembic upgrade head
```

### Create db revision

```console
alembic revision -m "<msg>"
```

### Run app

```console
python main.py
```

Then go to http address printed in console

### Test app

```console
pytest - n auto
```