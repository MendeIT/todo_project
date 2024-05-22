from sqlalchemy.orm import Session

from db.models import Todo
from api.schemas import todo


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Todo).offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()


def create_todo(db: Session, todo: todo.CreateTodoSchema):
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: todo.UpdateTodoSchema):
    """Добавить todo"""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    db_todo.completed = True if db_todo.completed is False else False
    db.commit()
    return db_todo
