from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from api.schemas.todo import (
    CreateTodoSchema,
    TodoSchema,
    UpdateTodoSchema
)
from auth.utils import read_jwt_token
from auth.schema import oauth2_scheme
from db.database import get_session
from db.models import Todo
from exceptions import ObjectDoesNotExistException, CustomExceptionModel


todo_router = APIRouter(
    prefix="/todos",
    tags=["ToDo"]
)


@todo_router.get("/", response_model=list[TodoSchema])
async def get_todos(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session)
):
    todos = await crud.get_all_todos(session=db, skip=skip, limit=limit)

    return list(todos)


@todo_router.get(
    "/{todo_id}",
    response_model=TodoSchema,
    status_code=status.HTTP_200_OK,
    summary="Get todo by ID.",
    description=("The endpoint returns todo_id by ID. "
                 "If the todo_id is doesn't exists,"
                 "an exception with the status code 404 is returned."),
    responses={
        status.HTTP_200_OK: {'model': TodoSchema},
        status.HTTP_404_NOT_FOUND: {'model': CustomExceptionModel},
    }
)
async def get_todo(
    todo_id: int,
    db: AsyncSession = Depends(get_session)
):
    todo = await crud.get_one_todo(session=db, todo_id=todo_id)

    if not todo:
        raise ObjectDoesNotExistException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The requested object does not exist.',
            message=(
                "You're trying to get an object that doesn't exist. "
                "Try entering a different object."
            )
        )

    return todo


@todo_router.post(
    "/",
    response_model=TodoSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_todo(
    todo: CreateTodoSchema,
    db: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme)
) -> Todo:

    payload = read_jwt_token(token)
    user_id = payload.get('user_id')

    new_todo = await crud.create_todo_for_user(
        session=db,
        todo=todo,
        user_id=user_id
    )

    return new_todo


@todo_router.put(
    "/{todo_id}",
    response_model=TodoSchema,
    status_code=status.HTTP_200_OK,
    summary="Update todo by ID.",
    description=("The endpoint update and returns todo_id by ID. "
                 "If the todo_id is doesn't exists,"
                 "an exception with the status code 404 is returned."),
    responses={
        status.HTTP_200_OK: {'model': TodoSchema},
        status.HTTP_404_NOT_FOUND: {'model': CustomExceptionModel},
    }
)
async def update_todo(
    todo_id: int,
    todo: UpdateTodoSchema,
    db: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme)
):
    payload = read_jwt_token(token)
    user_id = payload.get('user_id')

    new_todo = await crud.update_todo_for_user(
        session=db,
        todo_id=todo_id,
        todo=todo,
        user_id=user_id
    )

    if not new_todo:
        raise ObjectDoesNotExistException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The requested object does not exist.',
            message=(
                "You're trying to get an object that doesn't exist. "
                "Try entering a different object."
            )
        )

    return new_todo


@todo_router.delete(
    "/{todo_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete todo by ID.",
    description=("The endpoint delete todo_id by ID. "
                 "If the todo_id is doesn't exists,"
                 "an exception with the status code 404 is returned."),
)
async def delete_todo(
    todo_id: int,
    db: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme)
) -> JSONResponse:
    payload = read_jwt_token(token)
    user_id = payload.get('user_id')

    del_todo = await crud.delete_todo_for_user(
        session=db,
        todo_id=todo_id,
        user_id=user_id
    )

    if not del_todo:
        raise ObjectDoesNotExistException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The deleted object does not exist.',
            message=(
                "You're trying to delete an object that doesn't exist. "
                "Try entering a different object."
            )
        )

    return JSONResponse(
        content={'detail': f'A task id = {todo_id} was deleted.'},
        status_code=status.HTTP_200_OK
    )
