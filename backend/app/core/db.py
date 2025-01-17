# from typing import Any, Annotated, Generator

# from fastapi import Depends
# from sqlalchemy import Select, Insert, Update, CursorResult
# from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.models.User import User, UserCreate
from app.repositories.user import UserRepository

DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)
# engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))
engine = create_engine(DATABASE_URL, echo=False)

# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28


# class BaseModel(SQLModel):
#     ...


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = UserRepository.create(session=session,
                                     user_create=user_in)
