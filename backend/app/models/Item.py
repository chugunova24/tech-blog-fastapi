# from sqlmodel import Field, Relationship, SQLModel
from typing import Optional

from sqlmodel import Field, Relationship

from app.core.basemodel import BaseModel

# from .User import User
# from sqlmodel import SQLModel


# Shared properties
class ItemBase(BaseModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: Optional["User"] = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(BaseModel):
    data: list[ItemPublic]
    count: int
