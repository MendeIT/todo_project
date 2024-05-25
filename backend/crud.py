from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Todo
from api.schemas import todo as schema


def _check_DoesNotExists(object):
    """Ошибка. Искомый объект отсутствет в БД."""

    if object is None or object == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The requested object does not exist."
        )


async def get_all(session: AsyncSession, skip: int = 0, limit: int = 100):
    """GET. Получение списка из БД."""
    query = select(Todo).offset(skip).limit(limit)
    results = await session.execute(query)
    return results.scalars().all()


async def get_one(session: AsyncSession, object_id: int):
    """GET. Получение одного объекта из БД."""
    query = select(Todo).where(Todo.id == object_id)
    results = await session.execute(query)
    todo = results.scalar_one_or_none()
    _check_DoesNotExists(todo)

    return todo


async def create_one(
    session: AsyncSession,
    object: schema.CreateTodoSchema
) -> schema.TodoSchema:
    """POST. Создание и сохранение в БД."""
    new_todo = Todo(**object.model_dump())
    session.add(new_todo)
    await session.commit()
    await session.refresh(new_todo)

    return new_todo


async def update_one(
    session: AsyncSession,
    object_id: int,
    object: schema.UpdateTodoSchema
) -> Todo:
    """PUT. Обновление с сохранением в БД."""
    query = select(Todo).where(Todo.id == object_id)
    result = await session.execute(query)
    todo = result.scalar_one_or_none()
    _check_DoesNotExists(todo)
    todo.title = object.title
    todo.description = object.description
    todo.completed = object.completed
    await session.commit()

    return todo


async def delete_one(session: AsyncSession, object_id: int):
    """DELETE. Удаление из БД задачи."""
    query = delete(Todo).where(Todo.id == object_id)
    await session.execute(query)
    await session.commit()
