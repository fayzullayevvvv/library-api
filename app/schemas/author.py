from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AuthorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    bio: str = ""
    born_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class AuthorCreate(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    bio: str = ""
    born_date: datetime | None = None
