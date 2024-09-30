from fastapi import APIRouter
from service.pydantic_models import order_py_models
from db.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from service import models
from service.cruds import order_crud, order_item_crud, product_crud



router = APIRouter()

"""Установка зависимости открытия и закрытия сессии"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/orders/", response_model=List[order_py_models.OrderResponse], tags=["Orders"])
async def get_orders(db: Session = Depends(get_db)):
    order = order_crud.get_orders(db)
    return order

@router.get("/orders/{id}", response_model=order_py_models.OrderResponse, tags=["Orders"])
async def get_order_by_id(id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == id).first()
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order doesn't exist!"
        )
    order = order_crud.get_order_by_id(db=db, id=id)
    return order

@router.post("/orders/", response_model=order_py_models.OrderResponse, tags=["Orders"])
async def create_order(order: order_py_models.OrderRequest, db: Session = Depends(get_db)):
    order_items_list = dict(order)["order_item"]
    check_quantity_result = product_crud.check_quantity(db, order_items=order_items_list)
    if not check_quantity_result:
        db_order = order_crud.create_order(db)
        for element in order_items_list:
            order_item_crud.create_order_item(db, order_id=db_order.id, order_item_request=element)
            product_crud.decrease_quantity(db, id=element.product_id, quantity=element.quantity)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient quantity of product with id = {check_quantity_result}"
        )
    return db_order

@router.patch("/orders/{id}/status", response_model=order_py_models.OrderResponse, tags=["Orders"])
async def edit_order_by_id(id: int, order_status: order_py_models.StatusEnum, db: Session = Depends(get_db)):
    db_product = db.query(models.Order).filter(models.Order.id == id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order doesn't exist!"
        )
    return order_crud.edit_order(db=db, id=id, status=order_status)