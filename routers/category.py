from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

router = APIRouter(
    prefix="/category",
    tags=["Category"]
)

@router.post("", response_model=schemas.SchemaCategoryShow)
def add_category(new_category: schemas.SchemaCategoryFor, db: Session = Depends(get_db)):
    old_category = db.query(models.ModelCategory).filter(models.ModelCategory.name_category == new_category.name_category).first()
    if old_category:
        raise HTTPException(status_code=400, detail="This category already exists")
    
    category_db = models.ModelCategory(name_category=new_category.name_category)
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db

@router.get("/{category_id}")
def get_detail_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.ModelCategory).filter(models.ModelCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code="400", detail="Category not found")
    return {
        "id": category.id,
        "name_category": category.name_category,
        "list_product": category.all_products
    }