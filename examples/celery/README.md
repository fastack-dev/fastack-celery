# celery

Sample application using celery.

## Installation

Clone this repository then do:

```
poetry install
poetry shell
```

Install ``pipenv``:

```
pip install pipenv
```

Install all dependencies:

```
cd examples/celery
pipenv install
```

## Run application

Start all services in `docker-compose`:

```
docker-compose up -d
```

Run app:

```
fastack runserver
```

Open a new terminal, run `celery worker`:

```
celery -A app.main:celery worker -l info
```
