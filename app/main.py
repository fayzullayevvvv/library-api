from fastapi import FastAPI

from .database import engine, Base
from .dependencies import get_db


Base.metadata.create_all(engine)

print(get_db())

app = FastAPI(title="Library API")
