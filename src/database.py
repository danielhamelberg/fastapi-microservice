import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
   """
   Returns a database session.

   This function is a generator that yields a database session object.
   The session is automatically closed when the generator is done.

   Returns:
      SessionLocal: A database session object.

   """
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()
