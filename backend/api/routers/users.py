from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from api.schemas.users import UserCreateSchemas, UserReadSchemas
from auth.utils import hashed_password, read_jwt_token
from auth.schema import oauth2_scheme
from db.database import get_session
from exceptions import ObjectDoesNotExistException

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@user_router.get("/", response_model=list[UserReadSchemas])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session)
):
    users = await crud.get_all_user_with_todos(
        session=db,
        skip=skip,
        limit=limit
    )
    users_with_todos = []
    for user in users:
        user_dict = user.__dict__.copy()
        user_dict['items'] = user.todo
        users_with_todos.append(user_dict)

    return [UserReadSchemas(**user) for user in users_with_todos]


@user_router.post("/", response_model=UserReadSchemas)
async def create_user(
    user: UserCreateSchemas,
    db: AsyncSession = Depends(get_session)
):
    check_user = await crud.get_user_by_username(
        session=db,
        username=user.username
    )

    if check_user:
        if user.username == check_user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        if user.email == check_user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    password = hashed_password(user.password)

    new_user = await crud.create_user(
        session=db,
        user=user,
        hashed_password=password
    )

    return new_user


@user_router.get("/{user_id}", response_model=UserReadSchemas)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme)
):
    payload = read_jwt_token(token)
    user_id_from_token = payload.get('user_id')

    if user_id_from_token != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to view this user"
        )

    user = await crud.get_user_with_todos(session=db, user_id=user_id)

    if not user:
        raise ObjectDoesNotExistException(
            status_code=404,
            detail="User not found"
        )

    user_dict = user.__dict__.copy()
    user_dict['items'] = user.todo

    return UserReadSchemas.model_validate(user_dict)
