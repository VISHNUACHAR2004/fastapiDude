# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1) DATABASE_URL
# For SQLite (file-based DB) use this URL.
DATABASE_URL = "sqlite:///./users.db"

# 2) Engine - the core DB connection object
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # only needed for SQLite + threads
)

# 3) SessionLocal - a factory to create DB sessions (transactions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4) Base - the declarative base that your models will inherit from
Base = declarative_base()
