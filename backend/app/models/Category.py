from sqlmodel import Field

from app.core.basemodel import BaseModel


# Shared properties
class CategoryBase(BaseModel):
    name: str


# Database model, database table inferred from class name
class Category(CategoryBase, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)


# Properties to receive on category creation
class CategoryCreate(CategoryBase):
    ...


# Properties to receive on category creation
class CategoryUpdate(BaseModel):
    ...


# # Properties to receive on category update
# class CategoryUpdate(CategoryBase):
#     ...


# Properties to return via API, id is always required
class CategoryPublic(CategoryBase):
    id: int = Field(alias="category_id")


class CategoriesPublic(BaseModel):
    categories: list[CategoryPublic]
    count: int
