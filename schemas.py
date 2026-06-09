from pydantic import BaseModel

class SchemaProduct(BaseModel):
    name: str
    price: int
    is_ready: bool = True
    