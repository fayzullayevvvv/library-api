from typing import Annotated, List

from fastapi import APIRouter, Query

from app.dependencies import get_db, get_session
from app.crud.author import get_authors, create_author
from app.schemas.author import AuthorResponse, AuthorCreate

router = APIRouter(tags=["authors"])


@router.get("/api/authors", response_model=List[AuthorResponse], status_code=200)
async def get_authors_view(
    search: Annotated[str, Query()] = "",
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    # db = next(get_db())
    db = get_session()
    return get_authors(db, search, skip, limit)


@router.post("/api/authors", response_model=AuthorResponse)
async def create_author_view(data: AuthorCreate):
    # db = next(get_db())

    db = get_session()
    author = create_author(db, data)

    return author
