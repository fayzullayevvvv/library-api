from typing import List

from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter_by(username=username).first()


def create_user(db: Session, username: str, hash_password: str, role: str) -> User:
    user = User(username=username, hash_password=hash_password, role=role)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_users(db: Session) -> List[User]:
    return db.query(User).all()
