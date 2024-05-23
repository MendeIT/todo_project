import sys

import uvicorn
from fastapi import FastAPI

from api.routers.todo import todo_router
from db import database, models

# Создание таблиц в БД SQLite3
models.Base.metadata.create_all(database.engine)

app = FastAPI(debug=True)

app.include_router(todo_router)


def start_server():
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        sys.exit(0)
