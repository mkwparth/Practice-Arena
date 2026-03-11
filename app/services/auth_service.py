from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.models.auth_account import AuthAccount
from app.models.session_model import Session as DBSession

from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.utils.token import create_refresh_token


from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

def register_user(db, email: str, password: str, name: str):

    email = email.lower()

    try:

        user = User(
            email=email,
            name=name
        )

        db.add(user)
        db.flush()  # generates user.id without committing

        auth = AuthAccount(
            user_id=user.id,
            provider="email",
            provider_user_id=email,
            password_hash=hash_password(password)
        )

        db.add(auth)

        db.commit()

        db.refresh(user)

        return user

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

def login_user(db: Session, email: str, password: str):

    email = email.lower()

    auth = db.query(AuthAccount).filter(
        AuthAccount.provider == "email",
        AuthAccount.provider_user_id == email
    ).first()

    if not auth:
        return None

    if not verify_password(password, auth.password_hash):
        return None

    access_token = create_access_token({
        "user_id": auth.user_id
    })

    refresh_token = create_refresh_token()

    session = DBSession(
        user_id=auth.user_id,
        refresh_token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    db.add(session)
    db.commit()

    return access_token, refresh_token


def refresh_access_token(db: Session, refresh_token: str):

    session = db.query(DBSession).filter(
        DBSession.refresh_token == refresh_token
    ).first()

    if not session:
        return None

    if session.expires_at < datetime.utcnow():
        return None

    access_token = create_access_token({
        "user_id": session.user_id
    })

    return access_token