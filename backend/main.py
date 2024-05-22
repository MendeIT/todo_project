import sys

import uvicorn
from fastapi import FastAPI

from api.routers.todo import todo_router
from db import database, models

# Создание таблиц в БД SQLite3
models.Base.metadata.create_all(database.engine)

app = FastAPI()

app.include_router(todo_router)

if __name__ == "__main__":
    try:
        uvicorn.run(app="main:app")
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
