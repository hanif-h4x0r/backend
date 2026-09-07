from fastapi import FastAPI

app = FastAPI(title="Minimarket")

@app.get("/")
async def root():
	return {"message": "FastAPI is running brother!"}
