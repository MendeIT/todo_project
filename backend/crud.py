from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.models import Todo, User
from api.schemas.todo import CreateTodoSchema, UpdateTodoSchema
from api.schemas.users import UserCreateSchemas


async def get_all_todos(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100
):
    """Получение списка задач."""

    query = select(Todo).offset(skip).limit(limit)
    results = await session.execute(query)

    return results.scalars().all()


async def get_one_todo(
    session: AsyncSession,
    todo_id: int
) -> Todo | None:
    """Получение задачи по id."""

    query = select(Todo).where(Todo.id == todo_id)
    results = await session.execute(query)

    return results.scalar_one_or_none()


async def get_one_todo_by_author(
    session: AsyncSession,
    todo_id: int,
    user_id: int
) -> Todo | None:
    """Получение задачи автором."""

    query = select(Todo).where(Todo.id == todo_id, Todo.author_id == user_id)
    result = await session.execute(query)

    return result.scalar_one_or_none()


async def create_todo_for_user(
    session: AsyncSession,
    todo: CreateTodoSchema,
    user_id: int
) -> Todo:
    """Создание задачи и назначение пользователя как автора."""

    try:
        new_todo = Todo(
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            author_id=user_id
        )
        session.add(new_todo)
        await session.commit()
        await session.refresh(new_todo)
        return new_todo

    except Exception as error:
        await session.rollback()
        raise error


async def update_todo_for_user(
    session: AsyncSession,
    todo_id: int,
    todo: UpdateTodoSchema,
    user_id: int
) -> Todo | None:
    """Обновление задачи для пользователя."""

    existing_todo = await get_one_todo_by_author(session, todo_id, user_id)

    if not existing_todo:
        return None

    existing_todo.title = todo.title
    existing_todo.description = todo.description
    existing_todo.completed = todo.completed

    await session.commit()
    await session.refresh(existing_todo)

    return existing_todo


async def delete_todo_for_user(
    session: AsyncSession,
    todo_id: int,
    user_id: int
) -> int:
    """Удаление задачи автором."""

    query = delete(Todo).where(Todo.id == todo_id, Todo.author_id == user_id)
    result = await session.execute(query)
    await session.commit()

    return result.rowcount


async def get_all_user_with_todos(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100
):
    """Получение списка из пользователей с задачами."""

    query = select(User).options(
        joinedload(User.todo)
    ).offset(skip).limit(limit)
    results = await session.execute(query)

    return results.unique().scalars().all()


async def get_user_with_todos(
    session: AsyncSession,
    user_id: int
) -> User | None:
    """Получение пользователя с задачами."""

    query = select(User).options(
        joinedload(User.todo)
    ).where(User.id == user_id)

    results = await session.execute(query)
    return results.unique().scalar_one_or_none()


async def get_user_by_username(
    session: AsyncSession,
    username: str
) -> User | None:
    """Получение пользователя из БД по username."""

    query = select(User).where(User.username == username)
    result = await session.execute(query)

    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    user: UserCreateSchemas,
    hashed_password: bytes
) -> User:
    """Создание пользователя с хешированным паролем."""

    try:
        new_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user

    except Exception as error:
        await session.rollback()
        raise error
