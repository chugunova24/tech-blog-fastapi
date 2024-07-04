from sqlalchemy import func
from sqlmodel import Session, select

from app.models.Category import Category


class CategoryRepository:
    @staticmethod
    def is_exists(session: Session, category_name: str):
        statement = select(func.count(Category.id)).where(
            Category.name == category_name
        )
        return session.exec(statement).one()

    @staticmethod
    def create(session: Session, name: str):
        new_category = Category(name=name)
        session.add(new_category)
        session.commit()
        session.refresh(new_category)

        return new_category

    @staticmethod
    def get_all(session: Session):
        statement = select(Category)
        return session.exec(statement).all()
