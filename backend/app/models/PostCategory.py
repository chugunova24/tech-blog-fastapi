from sqlmodel import Field

from app.core.basemodel import BaseModel


# Shared properties
class PostCategoryBase(BaseModel):
    ...


# Database model, database table inferred from class name
class PostCategory(PostCategoryBase, table=True):
    __tablename__ = "post_category"

    id: int | None = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="posts.id", nullable=False)
    category_id: int = Field(foreign_key="categories.id", nullable=False)


class PostCategoryPublic(PostCategoryBase):
    id: int
    category_id: int
    name: str
