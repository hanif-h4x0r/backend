from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import SchemaCategoryShow, SchemaCategoryFor, SchemaProductCreate, SchemaProductShow
import models
from database import engine, get_db
from typing import Optional
from sqlalchemy import or_


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Endpoint Category

@app.post("/category", response_model=SchemaCategoryShow)
def add_category(new_category: SchemaCategoryFor, db: Session = Depends(get_db)):
    # Check at first is the name category already exists(for not duplicate)
    old_category = db.query(models.ModelCategory).filter(models.ModelCategory.name_category == new_category.name_category).first()
    if old_category:
        raise HTTPException(status_code=400, detail="This category already exists!")
    
    category_db = models.ModelCategory(name_category=new_category.name_category)
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db

# Get detail category
@app.post('/category/{category_id}')
def get_detail_category(category_id: int, db: Session = Depends(get_db)):
    #search that category in neon db based on id that user send
    category = db.query(models.ModelCategory).filter(models.ModelCategory.id == category_id).first()

    #if category not found, give it polite error
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    #if found return to the category with that id to user
    return {
        "id": category.id,
        "name_category": category.name_category,
        "list_product": category.all_products
    }


# Endpoint Product
@app.post("/add-product", response_model=SchemaProductShow)
def add_product(new_product: SchemaProductCreate, db: Session = Depends(get_db)):
    # Validation, check is id category that user input really exists in neon db
    check_category = db.query(models.ModelCategory).filter(models.ModelCategory.id == new_product.category_id).first()
    if not check_category:
        raise HTTPException(status_code=404, detail="Cannot add product, ID category didn'nt exists in neon database")
    # Is exists save the product
    product_db = models.ModelProduct(
        name=new_product.name,
        price=new_product.price,
        is_ready=new_product.is_ready,
        category_id=new_product.category_id
    )
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db

@app.get("/product")
def get_all_product(
    keyword: Optional[str] = None,
    limit: int = 10,
    skip: int = 0,
    db: Session = Depends(get_db)
):
    # Start with basic query to table product
    query = db.query(models.ModelProduct)

    # Filter search: if user type something in column keyword
    if keyword:
        # Mean search product that the name was contain keyword
        # .like() the func waas to make the word not sensitive big and small words
        query = query.filter(models.ModelProduct.name.ilike(f"%{keyword}%"))

        # Pagination: limit data with .limit() and .offside()
        # .limit(10) > just collect 10 data
        # .offside(0) > start with first data
        total_product = query.count()
        result_product = query.limit(limit).offset(skip).all()

        return {
            "total_find": total_product,
            "limit": limit,
            "skip": skip,
            "data": result_product
        }

@app.put("/change-product/{product_id}", response_model=SchemaProductShow)
def change_product(product_id: int, new_data: SchemaProductCreate, db: Session = Depends(get_db)):
    # look at old items in neon db
    old_product = db.query(models.ModelProduct).filter(models.ModelProduct.id == product_id).first()

    if not old_product:
        raise HTTPException(status_code=404, detail="Product not foound, can't edit")
    
    #New validation: check is new id category that user send really exists in database
    # make sure users dont move product to id category invisible that didn't exists
    check_category = db.query(models.ModelCategory).filter(models.ModelCategory.id == new_data.category_id).first()
    if not check_category:
        raise HTTPException(status_code=404, detail="can't edit, id category destiny is not registered")
    
    # if everything was right overwrite the old data to the new data
    old_product.name = new_data.name
    old_product.price = new_data.price
    old_product.is_ready = new_data.is_ready
    old_product.category_id = new_data.category_id # Move rack category here

    # Save permanent to database neon db
    db.commit()
    db.refresh(old_product) 

    return old_product   