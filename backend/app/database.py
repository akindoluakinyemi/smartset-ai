import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# -----------------------------
# ENGINE (connects Python ↔ PostgreSQL)
# -----------------------------
engine = create_engine(DATABASE_URL)

# -----------------------------
# SESSION (used for queries later)
# -----------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -----------------------------
# BASE (all models inherit from this)
# -----------------------------
Base = declarative_base()
