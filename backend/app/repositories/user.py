from typing import Any

from sqlalchemy import func
from sqlmodel import Session, select

from app.core.security import get_password_hash
from app.models.User import User, UserCreate, UserUpdate


class UserRepository:

    @staticmethod
    def get_by_id(session: Session,
                  user_id: int
                  ) -> User | None:
        user = session.get(User, user_id)
        return user

    @staticmethod
    def get_by_email(session: Session,
                     email: str
                     ) -> User | None:
        statement = select(User).where(User.email == email)
        session_user = session.exec(statement).first()
        return session_user

    @staticmethod
    def get_count_users(session: Session):
        count_statement = select(func.count()).select_from(User)
        return session.exec(count_statement).one()

    @staticmethod
    def get_users(session: Session,
                  skip: int,
                  limit: int
                  ) -> list[dict]:
        statement = select(User).offset(skip).limit(limit)
        users = session.exec(statement).all()
        return users

    @staticmethod
    def create(*, session: Session,
                    user_create: UserCreate) -> User:
        db_obj = User.model_validate(
            user_create,
            update={"hashed_password": get_password_hash(user_create.password)}
        )
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(*, session: Session,
               db_user: User,
               user_in: UserUpdate,
               extra_data: dict
               ) -> Any:
        # TODO: change extra_data input parameter
        user_data = user_in.model_dump(exclude_unset=True)
        # extra_data = {}
        if "password" in user_data:
            password = user_data["password"]
            hashed_password = get_password_hash(password)
            extra_data["hashed_password"] = hashed_password
        db_user.sqlmodel_update(user_data, update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def update_password(*, session: Session,
                        user: User,
                        new_password: str
                        ) -> None:
        hashed_password = get_password_hash(new_password)
        user.hashed_password = hashed_password
        session.add(user)
        session.commit()

    @staticmethod
    def delete(*, session: Session,
               user: User) -> None:
        # TODO: delete everything associated with the user
        # statement = delete(Item).where(col(Item.owner_id) == current_user.id)
        session.delete(user)
        session.commit()
