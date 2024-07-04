from typing import Any

from fastapi import APIRouter

from app.core.deps import SessionDep
from app.models.Post import PostCreate, PostPublic, PostsPublic, PostUpdate
from app.models.Security import Message
from app.models.User import User
from app.repositories.post import PostRepository
from app.services.post import PostServices

router = APIRouter()


@router.get("/", response_model=PostsPublic, response_model_exclude_none=True)
def get_posts(session: SessionDep, skip: int = 0, limit: int = 20) -> Any:
    """
    Retrieve posts.
    """
    posts = PostRepository.get_posts(session, skip, limit)

    return PostsPublic(posts=posts, count=len(posts))


@router.get("/{id}", response_model=PostPublic)
def get_post(session: SessionDep, id: int) -> Any:
    """
    Get post by ID.
    """
    post, categories = PostServices.get_post_by_id(session, id)

    return PostPublic(**post.model_dump(), categories=categories)


@router.post("/", response_model=PostPublic, status_code=201)
def create_post(
    session: SessionDep,
    # current_user: CurrentUser,
    post_in: PostCreate,
) -> Any:
    """
    Create new post.
    """
    mock_current_user = User(id=1)  # TODO: delete mocking

    new_post, categories = PostServices.create_post(
        session=session, current_user=mock_current_user, post_in=post_in
    )
    return PostPublic(**new_post.model_dump(), categories=categories)


@router.patch("/", response_model=PostPublic)
def update_post(
    session: SessionDep,
    # current_user: CurrentUser,
    post_in: PostUpdate,
) -> Any:
    """
    Update a post.
    """
    post, categories = PostServices.update_post(session=session, post_in=post_in)

    return PostPublic(**post.model_dump(), categories=categories)


@router.delete("/{id}")
def delete_post(
    session: SessionDep,
    # current_user: CurrentUser,
    id: int,
) -> Message:
    """
    Delete a post.
    """
    PostServices.delete_post(session, id)

    return Message(message="Post deleted successfully")


@router.get(
    "/search/{keyword}", response_model=PostsPublic, response_model_exclude_none=True
)
def search_posts(session: SessionDep, keyword: str) -> list[dict]:
    posts = PostServices.search_posts(session, keyword)

    return PostsPublic(posts=posts, count=len(posts))


@router.get("/random/", response_model=PostPublic)
def get_random_post(session: SessionDep) -> list[dict]:
    post, categories = PostServices.get_random_post(session)

    return PostPublic(**post.model_dump(), categories=categories)
