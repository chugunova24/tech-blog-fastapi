from sqlalchemy import delete
from sqlmodel import Session, select

from app.models.Category import Category
from app.models.PostCategory import PostCategory


class PostCategoryRepository:
    @staticmethod
    def get_categories_by_post(session: Session, post_id: int) -> list[dict | None]:
        statement = (
            select(PostCategory, Category.name)
            .filter(PostCategory.post_id == post_id)
            .join(Category, PostCategory.category_id == Category.id)
        )
        post_categories = session.exec(statement).all()

        # TODO: create def categories to share dict
        return [
            {
                "id": category[0].id,
                "category_id": category[0].category_id,
                "name": category[1],
            }
            for category in post_categories
        ]

    @staticmethod
    def bulk_insert(session: Session, new_categories: list[dict]) -> None:
        session.bulk_insert_mappings(PostCategory, new_categories)
        session.commit()

    @staticmethod
    def delete(session: Session, post_id: int) -> None:
        statement = delete(PostCategory).where(PostCategory.post_id == post_id)
        session.exec(statement)
        session.commit()
