from fastapi import FastAPI
from pydantic import BaseModel # This import was for build data schema

# Initialization fastapi application
app = FastAPI()

# Make schema data product with pydantic

class Product(BaseModel):
    name: str
    price: int
    is_ready: bool = True # default was true if user didn't input

database_product = [] #Temporary database

@app.get("/product")
def get_all_product():
    return {"total_product": len(database_product), "data": database_product}

@app.get('/')
def home():
    return {"message": "This is my first API"}


@app.post("/add-product")
def add_product(new_items: Product): # use schema product that we made
    # change data fromo pytdantic become ordinary dictionary, then save to our mini database
    product_dict = new_items.model_dump()
    database_product.append(product_dict)

    return {"message": "Product added successfully", "data_recorded": product_dict}