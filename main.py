from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import SchemaCategoryShow, SchemaCategoryFor, SchemaProductCreate, SchemaProductShow
import models
from database import engine, get_db

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
def get_all_product(db: Session = Depends(get_db)):
    all_product = db.query(models.ModelProduct).all()
    return {"total_product": len(all_product), "data": all_product}