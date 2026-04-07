from typing import Annotated

from fastapi import APIRouter, Query, Path, HTTPException, Body, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.crud.author import (
    get_authors,
    create_author,
    get_author_by_id,
    update_author_by_id,
    delete_author_by_id,
    get_author_books,
)
from app.schemas.author import (
    AuthorResponse,
    AuthorsResponse,
    Authorcreate,
    AuthorUpdate,
    AuthorBookResponse,
    AuthorBooksResponse,
)
from app.schemas.genre import GenreResponse
from app.models import Genre
from app.security import verify_token

router = APIRouter(tags=["authors"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get("/api/authors", response_model=AuthorsResponse, status_code=200)
async def get_authors_view(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    search: Annotated[str, Query()] = "",
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    authors = get_authors(db, search, skip, limit)

    response = AuthorsResponse(
        limit=limit, skip=skip, search=search, count=len(authors), result=authors
    )

    return response


@router.post("/api/authors", status_code=201)
async def create_author_view(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    data: Annotated[Authorcreate, Body],
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    author = create_author(
        db=db,
        first_name=data.first_name,
        last_name=data.last_name,
        bio=data.bio,
        born_date=data.born_date,
    )

    response = AuthorResponse(
        id=author.id,
        first_name=author.first_name,
        last_name=author.last_name,
        bio=author.bio,
        born_date=author.born_date,
    )

    return response


@router.get("/api/authors/{id}")
async def get_author_by_id_view(
    id: Annotated[int, Path(gt=0)],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    author = get_author_by_id(db=db, id=id)

    response = AuthorResponse(
        id=author.id,
        first_name=author.first_name,
        last_name=author.last_name,
        bio=author.bio,
        born_date=author.born_date,
    )

    return response


@router.patch("/api/authors/{id}")
async def update_author_by_id_view(
    id: Annotated[int, Path(gt=0)],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    data: Annotated[AuthorUpdate | None, Body] = None,
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    author = update_author_by_id(
        db=db,
        id=id,
        first_name=data.first_name,
        last_name=data.last_name,
        bio=data.bio,
        born_date=data.born_date,
    )

    response = AuthorResponse(
        id=author.id,
        first_name=author.first_name,
        last_name=author.last_name,
        bio=author.bio,
        born_date=author.born_date,
    )

    return response


@router.delete("/api/authors/{id}", status_code=204)
async def delete_author_by_id_view(
    id: Annotated[int, Path(gt=0)],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    delete_author_by_id(db=db, id=id)


@router.get("/api/authors/{id}/books")
async def get_author_books_view(
    id: Annotated[int, Path(gt=0)],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="invalid token.")

    author, books = get_author_books(db=db, id=id, skip=skip, limit=limit)

    author = AuthorResponse(
        id=author.id,
        first_name=author.first_name,
        last_name=author.last_name,
        bio=author.bio,
        born_date=author.born_date,
    )

    book_responses = []
    for book in books:
        book_genres = book.book_genres
        genres: list[Genre] = [b.genre for b in book_genres]

        genres = [
            GenreResponse(id=g.id, name=g.name, description=g.description)
            for g in genres
        ]

        book_response = AuthorBookResponse(
            id=book.id,
            title=book.title,
            published_year=book.published_year,
            author=author,
            genres=genres,
        )
        book_responses.append(book_response)

    return AuthorBooksResponse(
        limit=limit, skip=skip, count=len(books), result=book_responses
    )
