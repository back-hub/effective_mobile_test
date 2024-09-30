from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from .order_item_py_models import OrderItemResponse, OrderItemRequest

class StatusEnum(str, Enum):
    in_progress = "В процессе"
    sent = "Отправлен"
    delivered = "Доставлен"


class Order(BaseModel):
    pass
    

    class Config:
        orm_mode = True

class OrderResponse(Order):
    id: int
    status: str
    created_at: datetime
    items: List[OrderItemResponse]


class OrderRequest(Order):
    order_item: List[OrderItemRequest]

