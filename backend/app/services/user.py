from fastapi import HTTPException

from sqlmodel import Session

from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.models.Security import UpdatePassword
from app.models.User import UserCreate, User, UserUpdateMe, UserRegister
from app.repositories.user import UserRepository
from app.utils.utils import generate_new_account_email, send_email


class UserService:

    @staticmethod
    def get_by_id(session: Session,
                  user_id: int,
                  current_user: User
                  ) -> User:
        user = UserRepository.get_by_id(session=session,
                                        user_id=user_id)
        if user == current_user:
            return user
        if not current_user.is_superuser:
            raise HTTPException(status_code=403,
                                detail="The user doesn't have enough privileges")
        return user

    @staticmethod
    def get_users(session: Session,
                  skip: int,
                  limit: int):
        users = UserRepository.get_users(session=session,
                                         skip=skip,
                                         limit=limit)
        count = UserRepository.get_count_users(session=session)
        return users, count

    @staticmethod
    def create(session: Session,
               user_in: UserCreate
               ) -> User:
        user = UserRepository.get_by_email(session=session,
                                                email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system.",
            )

        user = UserRepository.create(session=session,
                                     user_create=user_in)
        if settings.emails_enabled and user_in.email:
            email_data = generate_new_account_email(email_to=user_in.email,
                                                    username=user_in.email,
                                                    password=user_in.password)
            send_email(email_to=user_in.email,
                       subject=email_data.subject,
                       html_content=email_data.html_content)
        return user

    @staticmethod
    def update(session: Session,
               user_in: UserUpdateMe,
               current_user: User
               ) -> User:
        if user_in.email:
            existing_user = UserRepository.get_by_email(session=session,
                                                             email=user_in.email)
            if existing_user and existing_user.id != current_user.id:
                raise HTTPException(
                    status_code=409,
                    detail="User with this email already exists"
                )
        db_user = UserRepository.update(session=session,
                                        db_user=current_user,
                                        user_in=user_in,
                                        extra_data={})

        return current_user

    @staticmethod
    def update_by_id(session: Session,
                     user_id: int,
                     user_in: UserUpdateMe
                     ) -> User:
        db_user = UserRepository.get_by_id(session=session,
                                           user_id=user_id)
        if not db_user:
            raise HTTPException(
                status_code=404,
                detail="The user with this id does not exist in the system",
            )
        if user_in.email:
            existing_user = UserRepository.get_by_email(session=session,
                                                             email=user_in.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=409, detail="User with this email already exists"
                )

        db_user = UserRepository.update(session=session,
                                        db_user=db_user,
                                        user_in=user_in,
                                        extra_data={})
        return db_user

    @staticmethod
    def update_password_me(session: Session,
                           body: UpdatePassword,
                           current_user: User
                           ) -> None:
        if not verify_password(body.current_password,
                               current_user.hashed_password):
            raise HTTPException(status_code=400,
                                detail="Incorrect password")
        if body.current_password == body.new_password:
            raise HTTPException(status_code=400,
                                detail="New password cannot be the same as the current one")

        UserRepository.update_password(session=session,
                                       user=current_user,
                                       new_password=body.new_password)

    @staticmethod
    def delete(session: Session,
               user: User
               ) -> None:
        if user.is_superuser:
            raise HTTPException(status_code=403,
                                detail="Super users are not allowed to delete themselves")
        UserRepository.delete(session=session,
                              user=user)

    @staticmethod
    def delete_by_id(session: Session,
                     user_id: int
                     ) -> None:
        user = UserRepository.get_by_id(session=session,
                                        user_id=user_id)
        if not user:
            raise HTTPException(status_code=404,
                                detail="User not found")
        if user.is_superuser:
            raise HTTPException(status_code=403,
                                detail="Super users are not allowed to delete themselves")
        UserRepository.delete(session=session,
                              user=user)

    @staticmethod
    def register(session: Session,
                 user_in: UserRegister
                 ) -> User:
        """
        Create new user without the need to be logged in.
        """
        if not settings.USERS_OPEN_REGISTRATION:
            raise HTTPException(status_code=403,
                                detail="Open user registration is forbidden on this server")
        user = UserRepository.get_by_email(session=session,
                                                email=user_in.email)
        if user:
            raise HTTPException(status_code=400,
                                detail="The user with this email already exists in the system")
        user_create = UserCreate.model_validate(user_in)
        user = UserRepository.create(session=session,
                                     user_create=user_create)
        return user
