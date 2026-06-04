import os
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

#load your hidden .env file
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

#build the pipeline to talk to neon database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Start fastapi app
app = FastAPI()

# Home
@app.get("/")
def home():
	return {"message": "FastAPI is running"}


#The database blueprint model
class UserTable(Base):
	__tablename__ = 'users' #This sets the actual table name inside neon

	id = Column(Integer, primary_key=True, index=True) #automaticly counts up (1, 2, 3...)
	username = Column(String(50), unique=True) #No two users can have the same name
	password = Column(String(255)) #stores the password text

@app.on_event("startup")
def create_tables_on_boot():
	#this commands tells neon: look at users table above and build it inside my cloud database
	Base.metadata.create_all(bind=engine)