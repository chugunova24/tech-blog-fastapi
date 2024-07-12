from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from app.core.config import settings
from app.core.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.security import get_password_hash, verify_password
from app.models.Item import (
    Item,
)
from app.models.Security import (
    Message,
    UpdatePassword,
)
from app.models.User import (
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.utils.utils import generate_new_account_email, send_email

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
def read_users(session: SessionDep,
               skip: int = 0,
               limit: int = 100
               ) -> Any:
    """
    Retrieve users.
    """
    users, count = UserService.get_users(session=session,
                                         skip=skip,
                                         limit=limit)
    return UsersPublic(data=users, count=count)


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
def create_user(*, session: SessionDep,
                user_in: UserCreate
                ) -> Any:
    """
    Create new user.
    """
    user = UserService.create(session=session,user_in=user_in)
    return user


@router.patch("/me",
              response_model=UserPublic)
def update_user_me(*, session: SessionDep,
                   user_in: UserUpdateMe,
                   current_user: CurrentUser
                   ) -> Any:
    """
    Update own user.
    """
    current_user = UserService.update(session=session,
                                      user_in=user_in,
                                      current_user=current_user)

    return current_user


@router.patch("/me/password",
              response_model=Message)
def update_password_me(*, session: SessionDep,
                       body: UpdatePassword,
                       current_user: CurrentUser
                       ) -> Any:
    """
    Update own password.
    """
    UserService.update_password_me(session=session,
                                   body=body,
                                   current_user=current_user)
    return Message(message="Password updated successfully")


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user


@router.delete("/me",
               response_model=Message)
def delete_user_me(session: SessionDep,
                   current_user: CurrentUser
                   ) -> Any:
    """
    Delete own user.
    """
    UserService.delete(session=session,
                       user=current_user)
    return Message(message="User deleted successfully")


@router.post("/signup",
             response_model=UserPublic)
def register_user(session: SessionDep,
                  user_in: UserRegister
                  ) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = UserService.register(session=session,
                                user_in=user_in)
    return user


@router.get("/{user_id}",
            response_model=UserPublic)
def read_user_by_id(session: SessionDep,
                    user_id: int,
                    current_user: CurrentUser
                    ) -> Any:
    """
    Get a specific user by id.
    """
    user = UserService.get_by_id(session=session,
                                 user_id=user_id,
                                 current_user=current_user)
    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
def update_user(
    *,
    session: SessionDep,
    user_id: int,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """

    db_user = UserService.update_by_id(session=session,
                                       user_id=user_id,
                                       user_in=user_in)
    return db_user


@router.delete("/{user_id}",
               dependencies=[Depends(get_current_active_superuser)])
def delete_user(session: SessionDep,
                # current_user: CurrentUser,
                user_id: int
                ) -> Message:
    """
    Delete a user.
    """
    UserService.delete_by_id(session=session,
                             user_id=user_id)
    return Message(message="User deleted successfully")
