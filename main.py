from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Import connection database and table that we made in another file
import models
from database import engine, get_db

app = FastAPI()

# Request to SQLAlchemy to automate create table product in Neon DB
models.Base.metadata.create_all(bind=engine)

# Schema pydantic for validation
class SchemaProduct(BaseModel):
    name: str 
    price: int
    is_ready: bool = True

# endpoint get to get all of product in neon databse
@app.get("/product")
def get_all_product(db: Session = Depends(get_db)):
    # Query sql ORM: SELECT * FROM product
    all_product = db.query(models.ModelProduct).all()
    return {"total_product": len(all_product), "data": all_product}

# endpoint post to post new product to neon database

@app.post("/product/add-product")
def add_product(new_product: SchemaProduct, db: Session = Depends(get_db)):
    # Change model from pydantic become model database SQLAlchemy
    product_db = models.ModelProduct{}