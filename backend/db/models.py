from sqlalchemy import (
    Boolean,
    Column,
    # ForeignKey,
    Integer,
    String
)
# from sqlalchemy.orm import relationship

from db.database import Base


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    # author_id = Column(Integer, ForeignKey("users.id"))

    # author = relationship("User", back_populates="todo")


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

#     items = relationship("Todo", back_populates="author")
