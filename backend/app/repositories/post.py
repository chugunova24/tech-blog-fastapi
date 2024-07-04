from datetime import datetime

import sqlalchemy
from fastapi import HTTPException
from sqlalchemy import func
from sqlmodel import Session, or_, select

from app.models.Post import Post, PostCreate, PostUpdate
from app.models.PostCategory import PostCategory


class PostRepository:
    @staticmethod
    def create(session: Session, user_id: int, post_in: PostCreate):
        dt_now = datetime.now()

        post = Post.model_validate(
            post_in,
            update={"owner_id": user_id, "created_at": dt_now, "updated_at": dt_now},
        )
        session.add(post)
        session.commit()
        session.refresh(post)

        if post_in.categories:
            categories: list[int] = list(set(post_in.categories))

            # categories to table row
            categories = [
                {"post_id": post.id, "category_id": int(x)} for x in categories
            ]
            try:
                session.bulk_insert_mappings(PostCategory, categories)
            except sqlalchemy.exc.IntegrityError:
                raise HTTPException(status_code=404, detail="The key does not exist")

        session.commit()

        return post

    @staticmethod
    def get_by_id(session: Session, post_id: int) -> Post | None:
        post = session.get(Post, post_id)

        return post

    @staticmethod
    def update(session: Session, post: Post, post_in: PostUpdate) -> Post | None:
        update_dict = post_in.model_dump(exclude_unset=True)
        update_dict["updated_at"] = datetime.now()

        post.sqlmodel_update(update_dict)
        session.add(post)
        session.commit()
        session.refresh(post)

        return post

    @staticmethod
    def delete(session: Session, post: Post) -> None:
        session.delete(post)
        session.commit()

    @staticmethod
    def filter_by_keyword(session: Session, keyword: str) -> list:
        pattern = f"%{keyword}%"
        statement = select(Post).filter(
            or_(Post.title.ilike(pattern), Post.content.ilike(pattern))
        )
        return session.exec(statement).all()

    @staticmethod
    def get_count_post(session: Session) -> int:
        statement = select(func.count(Post.id))
        return session.exec(statement).one()

    @staticmethod
    def get_post_by_offset(session: Session, offset: int) -> Post | None:
        post = session.exec(select(Post).offset(offset).limit(1)).one()

        return post

    @staticmethod
    def get_posts(session: Session, skip: int, limit: int) -> list[Post]:
        statement = select(Post).offset(skip).limit(limit)
        return session.exec(statement).all()
