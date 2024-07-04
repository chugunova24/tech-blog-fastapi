from fastapi import HTTPException
from sqlmodel import Session

from app.repositories.category import CategoryRepository


class CategoryServices:
    @staticmethod
    def create_category(session: Session, name: str) -> list[dict]:
        category_is_exists = CategoryRepository.is_exists(
            session=session, category_name=name
        )
        if category_is_exists:
            raise HTTPException(400, "Category with this name already exists")
        new_category = CategoryRepository.create(session=session, name=name)

        return new_category

    @staticmethod
    def get_all_categories(session: Session) -> list[dict]:
        return CategoryRepository.get_all(session)
