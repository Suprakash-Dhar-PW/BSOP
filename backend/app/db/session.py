import os
from sqlalchemy import create_all, create_engine
from sqlalchemy.orm import sessionmaker, Session

# Use PostgreSQL if env var is set, else fallback to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bsop_intelligence.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
