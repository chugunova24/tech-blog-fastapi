from sqlmodel import SQLModel


class BaseModel(SQLModel):
    ...


import app.models.User
import app.models.Item
import app.models.Security
import app.models.Post
import app.models.Category
import app.models.PostCategory
