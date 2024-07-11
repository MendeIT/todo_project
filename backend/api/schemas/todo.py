from pydantic import BaseModel, Field


class TodoBaseSchema(BaseModel):
    title: str = Field(min_length=3, max_length=64)
    description: str = Field(min_length=3, max_length=256)
    completed: bool = False


class CreateTodoSchema(TodoBaseSchema):
    ...


class UpdateTodoSchema(TodoBaseSchema):
    completed: bool


class DeleteTodoSchema(TodoBaseSchema):
    id: int


class TodoSchema(TodoBaseSchema):
    id: int
    author_id: int

    class Config:
        from_attributes = True
