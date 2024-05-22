from sqlalchemy.orm import Session

from db.models import Todo
from api.schemas import todo


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Todo).offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int):
    return db.query(Todo).get(todo_id)


def create_todo(db: Session, todo: todo.CreateTodoSchema) -> Todo:
    """Создание задачи."""
    try:
        db_todo = Todo(**todo.model_dump())
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
    except Exception as error:
        db.rollback()
        raise error
    else:
        return db_todo


def update_todo(db: Session, todo_id: int, todo: todo.UpdateTodoSchema):
    db_todo = db.query(Todo).get(todo_id)
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = True if todo.completed is True else False
    db.commit()
    return db_todo


def delete_todo(db: Session, todo_id: int):
    del_todo = db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()
    return del_todo
