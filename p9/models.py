from sqlalchemy import (
    Column, Integer, String, Boolean,
    DateTime, ForeignKey
)
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(300), nullable=False)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(300))
    priority = Column(String(20), nullable=False, default="Medium")
    is_completed = Column(Boolean, default=False)
    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    created_at = Column(
        DateTime,
        server_default=func.now()
    )