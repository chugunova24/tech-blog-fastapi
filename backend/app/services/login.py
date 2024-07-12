from datetime import timedelta
from typing import Any

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core import security
from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.models.Security import Token, NewPassword
from app.models.User import User
from app.repositories.user import UserRepository
from app.utils.utils import generate_password_reset_token, generate_reset_password_email, send_email, \
    verify_password_reset_token, EmailData


class Session:
    pass


class LoginService:

    @staticmethod
    def authenticate(*, session: Session,
                     email: str,
                     password: str
                     ) -> User | None:
        db_user = UserRepository.get_by_email(session=session,
                                                   email=email)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user

    @staticmethod
    def login_access_token(session: Session,
                           form_data: OAuth2PasswordRequestForm):
        """
        OAuth2 compatible token login, get an access token for future requests
        """
        user = LoginService.authenticate(session=session,
                                         email=form_data.username,
                                         password=form_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        elif not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        return user, access_token_expires

    @staticmethod
    def recover_password(email: str,
                         session: Session
                         ) -> None:
        """
        Password Recovery
        """
        user = UserRepository.get_by_email(session=session, email=email)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="The user with this email does not exist in the system.",
            )
        password_reset_token = generate_password_reset_token(email=email)
        email_data = generate_reset_password_email(
            email_to=user.email, email=email, token=password_reset_token
        )
        send_email(email_to=user.email,
                   subject=email_data.subject,
                   html_content=email_data.html_content)

    @staticmethod
    def reset_password(session: Session,
                       body: NewPassword
                       ) -> None:
        """
        Reset password
        """
        email = verify_password_reset_token(token=body.token)
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = UserRepository.get_by_email(session=session, email=email)
        if not user:
            raise HTTPException(status_code=404,
                                detail="The user with this email does not exist in the system.")
        elif not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        UserRepository.update_password(session=session,
                                       user=user,
                                       new_password=body.new_password)

    @staticmethod
    def recover_password_html_content(session: Session,
                                      email: str
                                      ) -> EmailData:
        """
        HTML Content for Password Recovery
        """
        user = UserRepository.get_by_email(session=session, email=email)

        if not user:
            raise HTTPException(status_code=404,
                                detail="The user with this username does not exist in the system.")
        password_reset_token = generate_password_reset_token(email=email)
        email_data = generate_reset_password_email(email_to=user.email,
                                                   email=email,
                                                   token=password_reset_token)

        return email_data
