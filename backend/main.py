import asyncio
import sys

import uvicorn
from fastapi import FastAPI

from api.routers.todo import todo_router
from core.config import settings
from db.database import init_models


app = FastAPI(debug=settings.DEBUG)

app.include_router(todo_router)


def start_server():
    uvicorn.run(
        app="main:app",
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        reload=settings.DEBUG
    )


async def main():
    await init_models() if settings.DEBUG else ...
    start_server()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
        message = 'Interrupted!'
        print(f'{message:_^50}')
        sys.exit(0)
