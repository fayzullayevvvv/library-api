from typing import List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate


def get_authors(
    db: Session, search: str = "", offset: int = 0, limit: int = 20
) -> List[Author]:
    q = db.query(Author)

    if search != "":
        pattern = f"%{search}%"

        q = q.filter(
            or_(
                Author.first_name.ilike(pattern),
                Author.last_name.ilike(pattern),
            )
        )

    authors = q.offset(offset).limit(limit).all()

    return authors


def create_author(db: Session, data: AuthorCreate) -> Author:
    author = Author(
        first_name=data.first_name,
        last_name=data.last_name,
        bio=data.bio,
        born_date=data.born_date,
    )

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_author(db: Session, id: int) -> Author | None:
    author = db.query(Author).get(id)

    return author


def update_author(db: Session, existing_author: Author, data: AuthorUpdate) -> Author:
    existing_author.first_name = (
        data.first_name if data.first_name else existing_author.first_name
    )
    existing_author.last_name = (
        data.last_name if data.last_name else existing_author.last_name
    )
    existing_author.bio = data.bio if data.bio else existing_author.bio
    existing_author.born_date = (
        data.born_date if data.born_date else existing_author.born_date
    )

    db.add(existing_author)
    db.commit()

    return existing_author
