from typing import Generator, Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database import SessionLocal
from app.security import verify_token
from app.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    user = db.query(User).filter_by(username=payload["username"]).first()

    if user is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    return user


def get_admin(user: Annotated[User, Depends(get_user)]) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="you are not admin.")

    return user


def get_editor(user: Annotated[User, Depends(get_user)]) -> User:
    if user.role != "editor":
        raise HTTPException(status_code=403, detail="you are not editor.")

    return user


def get_viewer(user: Annotated[User, Depends(get_user)]) -> User:
    if user.role != "viewer":
        raise HTTPException(status_code=403, detail="you are not viewer.")

    return user
