# README

1. Start `redis`.

    ```bash
    docker run -d -p 6379:6379 redis

    ```
1. Start `celery`.

    ```bash
    celery -A app.celery worker -l info
    ```
1. Start `flask`.

    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run
    ```