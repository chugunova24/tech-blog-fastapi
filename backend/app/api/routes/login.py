from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

# from app import crud
from app.core import security
from app.core.config import settings
from app.core.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core.security import get_password_hash
from app.models.Security import Message, NewPassword, Token
from app.models.User import UserPublic, User
from app.repositories.user import UserRepository
from app.services.login import LoginService
from app.utils.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(session: SessionDep,
                       form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user, access_token_expires = LoginService.login_access_token(session=session,
                                                                 form_data=form_data)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> User:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}")
def recover_password(email: str,
                     session: SessionDep
                     ) -> Message:
    """
    Password Recovery
    """
    LoginService.recover_password(session=session,
                                  email=email)
    return Message(message="Password recovery email sent")


@router.post("/reset-password/")
def reset_password(session: SessionDep,
                   body: NewPassword
                   ) -> Message:
    """
    Reset password
    """
    LoginService.reset_password(session=session,
                                body=body)
    return Message(message="Password updated successfully")


@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
)
def recover_password_html_content(email: str, session: SessionDep) -> Any:
    """
    HTML Content for Password Recovery
    """
    email_data = LoginService.recover_password_html_content(
        session=session,
        email=email
    )
    return HTMLResponse(
        content=email_data.html_content,
        headers={"subject:": email_data.subject}
    )
