from pydantic import BaseModel, Field


class TodoBaseSchema(BaseModel):
    title: str = Field(min_length=3, max_length=60)
    description: str = Field(min_length=3, max_length=250)


class CreateTodoSchema(TodoBaseSchema):
    ...


class UpdateTodoSchema(TodoBaseSchema):
    completed: bool


class DeleteTodoSchema(TodoBaseSchema):
    id: int


class TodoSchema(TodoBaseSchema):
    id: int
    completed: bool = False

    class Config:
        from_attributes = True
