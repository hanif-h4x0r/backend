from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship # Import this module to make a bridge connection
from database import Base

# It is will become table named Product in your neon
class ModelProduct(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
    is_ready = Column(Boolean, default=True)
    
    # Connect this product to ID in table category
    category_id = Column(Integer, ForeignKey("category.id"))

    # Invisible bridge: from product can directly know they included in which category
    the_category = relationship("ModelCategory", back_populates="all_products")


class ModelCategory(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name_category = Column(String, unique=True, index=True) #Example electronic

    # Invisible bridge, so from category can directly call the producs
    all_products = relationship("ModelProduct", back_populates="the_category")

