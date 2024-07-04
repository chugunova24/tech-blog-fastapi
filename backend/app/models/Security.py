# from sqlmodel import Field, Relationship, SQLModel
from app.core.basemodel import BaseModel

# from sqlmodel import SQLModel


class UpdatePassword(BaseModel):
    current_password: str
    new_password: str


# Generic message
class Message(BaseModel):
    message: str


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: int | None = None


class NewPassword(BaseModel):
    token: str
    new_password: str
