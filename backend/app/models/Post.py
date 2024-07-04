from datetime import datetime

from sqlmodel import Field

from app.core.basemodel import BaseModel
from app.models.PostCategory import PostCategoryPublic

# from app.models.Category import CategoryPublic


# from .User import User
# from sqlmodel import SQLModel


# Shared properties
class PostBase(BaseModel):
    title: str
    content: str


# Database model, database table inferred from class name
class Post(PostBase, table=True):
    __tablename__ = "posts"

    id: int | None = Field(default=None, primary_key=True, alias="post_id")
    owner_id: int = Field(
        foreign_key="user.id", nullable=False
    )  # TODO: вместо int установить UUID
    created_at: datetime
    updated_at: datetime  # TODO: onupdate отсутствует

    # categories: list[Category] | None = Relationship(back_populates="posts")


# Properties to receive on post creation
# TODO: создавать пост может только зарегистрированный пользователь
class PostCreate(PostBase):
    categories: list[int] = None


# Properties to receive on post update
# TODO: обновлять пост может только зарегистрированный пользователь
class PostUpdate(PostBase):
    id: int
    title: str | None = None
    content: str | None = None
    categories: list[int] = None


# Properties to return via API, id is always required
class PostPublic(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    categories: list[PostCategoryPublic] = None


class PostsPublic(BaseModel):
    posts: list[PostPublic]
    count: int
