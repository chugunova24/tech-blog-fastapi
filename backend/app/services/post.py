import random

from fastapi import HTTPException
from sqlmodel import Session

from app.models.Post import Post, PostCreate, PostUpdate
from app.models.User import User
from app.repositories.post import PostRepository
from app.repositories.post_category import PostCategoryRepository


class PostServices:
    @staticmethod
    def get_posts(session: Session, skip: int, limit: int) -> list[dict]:
        return PostRepository.get_posts(session, skip, limit)

    @staticmethod
    def get_post_by_id(session: Session, id: int) -> list[dict]:
        post = PostRepository.get_by_id(session=session, post_id=id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        categories = PostCategoryRepository.get_categories_by_post(
            session=session, post_id=post.id
        )
        return post, categories

    @staticmethod
    def create_post(session: Session, current_user: User, post_in: PostCreate) -> Post:
        new_post = PostRepository.create(
            session=session, user_id=current_user.id, post_in=post_in
        )
        categories = PostCategoryRepository.get_categories_by_post(
            session=session, post_id=new_post.id
        )

        return new_post, categories

    @staticmethod
    def update_post(session: Session, post_in: PostUpdate) -> Post:
        # TODO: change update post with categories add and delete actions
        post = PostRepository.get_by_id(session=session, post_id=post_in.id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        PostRepository.update(session=session, post=post, post_in=post_in)

        categories_exists = PostCategoryRepository.get_categories_by_post(
            session=session, post_id=post.id
        )

        categories_exists = [x["category_id"] for x in categories_exists]

        if post_in.categories:
            categories: set[int] = set(post_in.categories)
            new_categories = set(categories).difference(categories_exists)

            if new_categories:
                new_categories = [
                    {"post_id": post.id, "category_id": int(x)} for x in new_categories
                ]

                PostCategoryRepository.bulk_insert(
                    session=session, new_categories=new_categories
                )
            else:
                raise HTTPException(status_code=400, detail="The key already exist")

        categories = PostCategoryRepository.get_categories_by_post(
            session=session, post_id=post.id
        )

        return post, categories

    @staticmethod
    def delete_post(session: Session, id: int) -> None:
        post = PostRepository.get_by_id(session=session, post_id=id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        PostCategoryRepository.delete(session=session, post_id=post.id)
        PostRepository.delete(session=session, post=post)

    @staticmethod
    def search_posts(session: Session, keyword: str) -> list[dict]:
        # TODO: add paginator
        return PostRepository.filter_by_keyword(session=session, keyword=keyword)

    @staticmethod
    def get_random_post(session: Session) -> list[dict]:
        count = PostRepository.get_count_post(session)
        if count == 0:
            raise HTTPException(status_code=404, detail="No posts")

        offset = random.randint(0, count - 1)
        post = PostRepository.get_post_by_offset(session=session, offset=offset)
        categories = PostCategoryRepository.get_categories_by_post(
            session=session, post_id=post.id
        )

        return post, categories
