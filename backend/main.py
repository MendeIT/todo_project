import sys

import uvicorn
from fastapi import FastAPI

from api.routers.todo import todo_router
from core.config import settings
from db import database, models

# Создание таблиц в БД SQLite3
models.Base.metadata.create_all(database.engine)

app = FastAPI(debug=settings.DEBUG)

app.include_router(todo_router)


def start_server():
    uvicorn.run(
        app="main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        sys.exit(0)
