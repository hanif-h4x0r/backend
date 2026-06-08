from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# It is will become table named Product in your neon
class ModelProduct(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
    is_ready = Column(Boolean, default=True)