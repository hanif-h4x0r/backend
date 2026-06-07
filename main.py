from fastapi import FastAPI

# Initialization fastapi application
app = FastAPI()

# Make endpoint, method(GET, Path: "/")
@app.get("/")
def home():
    return {"message": "Hello world, this is my first API!"}

# Create a second endpoint for looking at user data based on user_id
@app.get("/user/{user_id}")
def get_user(user_id: int):
    # example collect data from database
    return {
        "user_id": user_id,
        "name": "Hanif",
        "status": "Active"
    }
