import asyncio
import sys

import uvicorn
from fastapi import FastAPI

from api.routers.todo import todo_router
from api.routers.users import user_router
from auth.schema import auth_router
from core.config import settings
from db.database import init_models  # noqa
from exceptions import setup_exception_handlers

app = FastAPI(debug=settings.DEBUG)

app.include_router(todo_router)
app.include_router(user_router)
app.include_router(auth_router)

setup_exception_handlers(app)


def start_server():
    uvicorn.run(
        app="main:app",
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        reload=settings.DEBUG
    )


async def main():
    # if settings.DEBUG:
    #     logger.info("Функция init_models() запущена")
    #     await init_models()
    start_server()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
        message = 'Interrupted!'
        print(f'{message:_^50}')
        sys.exit(0)
