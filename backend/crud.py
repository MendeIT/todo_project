from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.models import Todo
from api.schemas import todo


def _check_DoesNotExists(todo: Todo) -> HTTPException:
    """Ошибка. Искомый объект отсутствет в БД."""

    if todo is None or todo == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The requested object does not exist."
        )

    pass


def get_todos(db: Session, skip: int = 0, limit: int = 100) -> list[Todo]:
    """GET. Получение списка задач из БД."""
    return db.query(Todo).offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int) -> Todo:
    """GET. Получение задачи из БД."""
    db_todo = db.query(Todo).get(todo_id)

    _check_DoesNotExists(db_todo)

    return db_todo


def create_todo(db: Session, todo: todo.CreateTodoSchema) -> Todo:
    """POST. Создание задачи и сохранение в БД."""
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


def update_todo(
    db: Session,
    todo_id: int,
    todo: todo.UpdateTodoSchema
) -> Todo:
    """PUT. Обновление/выполнение задачи с сохранением в БД."""

    db_todo = db.query(Todo).get(todo_id)

    _check_DoesNotExists(db_todo)

    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = True if todo.completed is True else False
    db.commit()

    return db_todo


def delete_todo(db: Session, todo_id: int):
    """DELETE. Удаление из БД задачи."""

    del_todo = db.query(Todo).filter(Todo.id == todo_id).delete()

    _check_DoesNotExists(del_todo)

    db.commit()
