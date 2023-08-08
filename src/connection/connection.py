from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

from dotenv import load_dotenv
from os import environ

load_dotenv()

DB_URL= environ.get("CONNECTION_STRING")

engine = create_engine(DB_URL, poolclass=QueuePool, pool_size=10, max_overflow=20) # type: ignore

# Create the session factory with scoped_session
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
