from pydantic import BaseModel
from .product_py_models import ProductResponse


class OrderItem(BaseModel):
    
    quantity: int

class OrderItemResponse(OrderItem):
    id: int
    product: ProductResponse

class OrderItemRequest(OrderItem):
    product_id: int

