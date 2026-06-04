import os
from fastapi import FastAPI, Depends
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

# Action 3 the action route (save to neon)

from pydantic import BaseModel
from sqlalchemy.orm import Session

# Create pydantic from blueprint

class UserCreateFrom(BaseModel):
	username: str
	password: str

# Helper function to open and close a database session automatically

def get_db_session():
	db_session = Session(bind=engine) # Open the phone line
	try:
		yield db_session # Give the phone line to our route below
	finally:
		db_session.close() # Hang up the phone line when done

# The web route to register a user

@app.post('/register')
def register_new_user(incoming_data: UserCreateFrom, db: Session = Depends(get_db_session)):

	# Turn the incoming data into a row matching our UserTable layout
	new_row = UserTable(
		username=incoming_data.username,
		password=incoming_data.password
	)


	# Tell the database session to stage this new row
	db.add(new_row)

	# Click save (commit) permanently to neon!
	db.commit()

	# Refresh our row to grab the unique ID neon just generated for it
	db.refresh(new_row)

	return {
		"message": "User successfuly added to our neon database",
		"database_id": new_row.id,
		"registered_username": new_row.username
	}
