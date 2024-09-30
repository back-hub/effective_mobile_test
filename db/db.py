from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

DB_NAME = os.environ["DB_NAME"]
USER_NAME = os.environ["USER_NAME"]
PASSWORD = os.environ["PASSWORD"]
DB_HOST = os.environ["DB_HOST"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER_NAME}:{PASSWORD}@{DB_HOST}/{DB_NAME}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


data = SessionLocal()