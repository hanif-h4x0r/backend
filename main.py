from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import SchemaProduct

# Import connection database and table that we made in another file
import models
from database import engine, get_db

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI is running!"}

# Request to SQLAlchemy to automate create table product in Neon DB
models.Base.metadata.create_all(bind=engine)

# endpoint get to get all of product in neon databse
@app.get("/product")
def get_all_product(db: Session = Depends(get_db)):
    # Query sql ORM: SELECT * FROM product
    all_product = db.query(models.ModelProduct).all()
    return {"total_product": len(all_product), "data": all_product}

# endpoint post to post new product to neon database
@app.post("/product/add-product")
def add_product(new_product: SchemaProduct, db: Session = Depends(get_db)):
    # Change data from pydantic become model database SQLAlchemy
    product_db = models.ModelProduct(
        name=new_product.name,
        price=new_product.price,
        is_ready=new_product.is_ready
    )

@app.get("/product/{product_id}")
def get_one_product(product_id: int, db: Session = Depends(get_db)):
    # search to neon db use query command orm
    # mean: SELECT * FROM product WHERE id = product_id LIMIT 1;
    product = db.query(models.ModelProduct).filter(models.ModelProduct.id == product_id).first()

    # Conditioning if product was not found
    if not product:
        # We shot httpexception here
        raise HTTPException(status_code=404, detail="Product not found")
    
    # if found, return data to user
    return {"message": "Product found", "data": product}

@app.delete("/product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # Looking for items in database is it exists or not
    product_target = db.query(models.ModelProduct).filter(models.ModelProduct.id == product_id).first()

    # if item not found, give them polite error
    if not product_target:
        raise HTTPException(status_code=404, detail='Cannot delete, items not found')
    
    # if item found, lets execute delete command
    db.delete(product_target)
    db.commit()

    # return success delete items
    return {"message": f"Product with this ID {product_id} Successfuly deleted"}


    # Proses insert data to database Neon(INSERT INTO)
    db.add(product_db) # Add to queue
    db.commit() # Save or commit permanent to neon Database
    db.refresh(product_db) # Collect the latest data from neon DB (to get ID automate)

    return {"message": "Data successfuly saved in neon DB!", "data": product_db}