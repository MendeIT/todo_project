from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class CustomExceptionModel(BaseModel):
    """Модель ответов на ошибки."""
    status_code: int
    er_message: str
    er_details: str


class ObjectDoesNotExistException(HTTPException):
    """Заправшиваемый объект отсутствует."""
    def __init__(self, detail: str, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message


class CustomExceptionHandler:
    @staticmethod
    def init_exception_does_not_exist(app: FastAPI):
        @app.exception_handler(ObjectDoesNotExistException)
        async def object_does_not_exist_exception_handler(
            request: Request,
            exc: ObjectDoesNotExistException
        ) -> JSONResponse:
            """Обработчик отсутствует в БД."""
            error = jsonable_encoder(
                CustomExceptionModel(
                    status_code=exc.status_code,
                    er_message=exc.message,
                    er_details=exc.detail
                )
            )
            return JSONResponse(status_code=exc.status_code, content=error)

    @staticmethod
    def init_global_exception_handler(app: FastAPI):
        @app.exception_handler(Exception)
        async def global_exception_handler(
            request: Request,
            exc: Exception
        ) -> JSONResponse:
            """Обработчик глобальных исключений,
            который "ловит" все необработанные исключения."""

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "detail": str(exc)
                }
            )


def setup_exception_handlers(app: FastAPI):
    """Инициализация обработчиков исключений."""
    CustomExceptionHandler.init_exception_does_not_exist(app)
    CustomExceptionHandler.init_global_exception_handler(app)
