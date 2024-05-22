from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
from db.database import get_db
from api.schemas.todo import CreateTodoSchema, TodoSchema


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


@todo_router.get("/{todo_id}", response_model=TodoSchema)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.get_todo(db, todo_id)


@todo_router.post("/", response_model=TodoSchema)
def create_todo(todo: CreateTodoSchema, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)


@todo_router.put("/{todo_id}", response_model=TodoSchema)
def update_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.update_todo(db, todo_id)
