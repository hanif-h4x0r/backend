from pydantic import BaseModel
from typing import Optional

# Schema for category
class SchemaCategoryFor(BaseModel):
    name_category: str

class SchemaCategoryShow(BaseModel):
    id: int
    name_category: str

    class Config:
        from_attributes = True # So pydantic can read data directly from sqlalchemy orm

# Schema for product
class SchemaProductCreate(BaseModel):
    name: str
    price: int
    is_ready: bool = True
    category_id: int # Input required: so when we input product, we will know the product include to which category

class SchemaProductShow(BaseModel):
    id:  int
    name: str
    price: int
    is_ready: bool
    category_id = int
    the_category = Optional[SchemaCategoryShow] = None # The great feature, so when we collect product, the category itself also show themselves

    class Config:
        from_attributes = True
        
