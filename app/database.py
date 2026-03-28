from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings


url = URL.create(
    drivername="postgresql+psycopg2",
    host=settings.db_host,
    port=settings.db_port,
    username=settings.db_user,
    password=settings.db_pass,
    database=settings.db_name,
)
engine = create_engine(url)
SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
