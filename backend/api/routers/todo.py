from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import crud
from api.schemas.todo import (CreateTodoSchema,
                              TodoSchema,
                              UpdateTodoSchema)
from db.database import get_db


todo_router = APIRouter(
    prefix="/todos",
    tags=["ToDo"]
)


@todo_router.get("/", response_model=list[TodoSchema])
def get_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_todos(db, skip=skip, limit=limit)


@todo_router.get(
    "/{todo_id}",
    response_model=TodoSchema,
    status_code=status.HTTP_200_OK
)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.get_todo(db, todo_id)


@todo_router.post(
    "/",
    response_model=TodoSchema,
    status_code=status.HTTP_201_CREATED
)
def create_todo(todo: CreateTodoSchema, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)


@todo_router.put(
    "/{todo_id}",
    response_model=TodoSchema,
    status_code=status.HTTP_200_OK
)
def update_todo(
    todo_id: int,
    todo: UpdateTodoSchema,
    db: Session = Depends(get_db)
):
    return crud.update_todo(db, todo_id, todo)


@todo_router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    crud.delete_todo(db, todo_id)
    return JSONResponse(
        content={'detail': f'A task id \"{todo_id}\" was deleted.'}
    )
