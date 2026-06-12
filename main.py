from fastapi import FastAPI
import models
from database import engine
from routers import product, category

app = FastAPI(title="Shop API")

models.Base.metadata.create_all(bind=engine)

app.include_router(product.router)
app.include_router(category.router)

@app.get("/")
def home():
    return {"message": "FastAPI is running"}
