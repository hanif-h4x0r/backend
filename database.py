import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base # Safe way for all version
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Get link database from .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine and session for connection to postgreql
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is blueprint which we will use to create table
Base = declarative_base()

# Fungtion to help open-close connection to database automatically
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Database error: {e}")
        raise
    finally:
        db.close()