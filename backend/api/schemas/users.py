from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, PositiveInt, StrictBool

from api.schemas.todo import TodoSchema


class UserBaseSchemas(BaseModel):
    username: str = Field(min_length=4, max_length=16)
    email: EmailStr


class UserCreateSchemas(UserBaseSchemas):
    password: str = Field(
        min_length=8,
        max_length=32,
        pattern=r"((\S)(\w))+.{7,64}"
    )


class UserSchemas(UserBaseSchemas):
    id: PositiveInt
    is_active: StrictBool = True
    date_joined: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True


class UserReadSchemas(UserSchemas):
    items: list[TodoSchema] = []

    class Config:
        from_attributes = True


class UserLoginSchemas(BaseModel):
    username: str
    password: str
