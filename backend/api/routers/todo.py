from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from api.schemas.todo import (CreateTodoSchema,
                              TodoSchema,
                              UpdateTodoSchema)
from db.database import get_session


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
    todos = await crud.get_all(db, skip=skip, limit=limit)

    return list(todos)


@todo_router.get(
    "/{todo_id}",
    response_model=TodoSchema,
    status_code=status.HTTP_200_OK
)
async def get_todo(todo_id: int, db: AsyncSession = Depends(get_session)):
    todo = await crud.get_one(db, todo_id)

    return todo


@todo_router.post(
    "/",
    response_model=TodoSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_todo(
    todo: CreateTodoSchema,
    db: AsyncSession = Depends(get_session)
) -> TodoSchema:
    new_todo = await crud.create_one(db, todo)
    return new_todo


@todo_router.put(
    "/{todo_id}",
    response_model=TodoSchema,
    status_code=status.HTTP_200_OK
)
async def update_todo(
    todo_id: int,
    todo: UpdateTodoSchema,
    db: AsyncSession = Depends(get_session)
):
    new_todo = await crud.update_one(db, todo_id, todo)
    return new_todo


@todo_router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_session)):
    await crud.delete_one(db, todo_id)
    return JSONResponse(
        content={'detail': f'A task id \"{todo_id}\" was deleted.'}
    )
