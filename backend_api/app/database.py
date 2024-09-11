from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
from sqlalchemy.exc import OperationalError

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

def get_engine(retries=5, delay=2):
    for attempt in range(retries):
        try:
            engine = create_engine(SQLALCHEMY_DATABASE_URL)
            # Attempt a connection
            with engine.connect() as conn:
                pass
            return engine
        except OperationalError:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()