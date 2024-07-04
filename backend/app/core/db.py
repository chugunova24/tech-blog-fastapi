# from typing import Any, Annotated, Generator

# from fastapi import Depends
# from sqlalchemy import Select, Insert, Update, CursorResult
# from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models.User import User, UserCreate

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
        user = crud.create_user(session=session, user_create=user_in)


# if current_user.is_superuser:
#     count_statement = select(func.count()).select_from(Item)
#     count = session.exec(count_statement).one()
#     statement = select(Item).offset(skip).limit(limit)
#     items = session.exec(statement).all()
# else:
#     count_statement = (
#         select(func.count())
#         .select_from(Item)
#         .where(Item.owner_id == current_user.id)
#     )
#     count = session.exec(count_statement).one()
#     statement = (
#         select(Item)
#         .where(Item.owner_id == current_user.id)
#         .offset(skip)
#         .limit(limit)
#     )
#     items = session.exec(statement).all()


# SessionDep = Annotated[Session, Depends(get_db)]

# def fetch_one(session: SessionDep, statement: Select | Insert | Update) -> dict[str, Any] | None:
#     result = session.exec(statement)
#     return result.one() # if result.rowcount > 0 else None


# async def fetch_one(select_query: Select | Insert | Update) -> dict[str, Any] | None:
#     async with engine.begin() as conn:
#         cursor: CursorResult = await conn.execute(select_query)
#         return cursor._asdict() if cursor.rowcount > 0 else None


# async def fetch_all(select_query: Select | Insert | Update) -> list[dict[str, Any]]:
#     async with engine.begin() as conn:
#         cursor: CursorResult = await conn.execute(select_query)
#         return [r._asdict() for r in cursor.all()]
#
#
# async def execute(select_query: Insert | Update) -> None:
#     async with engine.begin() as conn:
#         await conn.execute(select_query)
