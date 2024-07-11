from sqlalchemy import (Boolean,
                        Column,
                        DateTime,
                        ForeignKey,
                        Integer,
                        String)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    author = relationship("User", back_populates="todo")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime(timezone=True), server_default=func.now())

    todo = relationship("Todo", back_populates="author")
