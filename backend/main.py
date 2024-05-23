import sys

import uvicorn
from fastapi import FastAPI

from api.routers.todo import todo_router
from core.config import settings
from db import database

database.init_db()

app = FastAPI(debug=settings.DEBUG)

app.include_router(todo_router)


def start_server():
    uvicorn.run(
        app="main:app",
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        reload=settings.DEBUG
    )


if __name__ == "__main__":
    try:
        start_server()
    except Exception:
        message = 'Interrupted!'
        print(f'{message:_^50}')
        sys.exit(0)
