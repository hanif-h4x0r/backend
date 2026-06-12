from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
import models, schemas
from database import get_db

# Create object APIRouter special for product
# prefix="/product" means all url in this file automate in word /product
# tags["product"] mean to group the menu in swagger become neat

router = APIRouter(
    prefix="/product",
    tags=["product"]
)

@router.post("/add", response_model=schemas.SchemaProductShow)
def add_product(new_items: schemas.SchemaProductCreate, db: Session = Depends(get_db)):
    check_category = db.query(models.ModelCategory).filter(models.ModelCategory.id == new_items.category_id).first()
    if not check_category:
        raise HTTPException(status_code=404, detail="ID Category not found")
    
    product_db = models.ModelProduct(
        name=new_items.name,
        price=new_items.price,
        is_ready=new_items.is_ready,
        category_id=new_items.category_id
    )
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db

@router.get("", response_model=List[schemas.SchemaProductShow])
def get_all_product(
    keyword: Optional[str] = None,
    limit: int = 10,
    skip: int = 0,
    db: Session = Depends(get_db)
    ):
    query = db.query(models.ModelProduct)
    if keyword:
        query = query.filter(models.ModelProduct.name.ilike(f"%{keyword}%"))
    return query.limit(limit).offset(skip).all()
    
    
