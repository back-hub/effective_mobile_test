from fastapi import APIRouter
from service.pydantic_models import product_py_models
from db.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from service import models
from service.cruds import product_crud



router = APIRouter()


"""Установка зависимости открытия и закрытия сессии"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/products/", response_model=List[product_py_models.ProductResponse], tags=["Products"])
async def get_products(db: Session = Depends(get_db)):
    product = product_crud.get_products(db)
    return product

@router.get("/products/{id}", response_model=product_py_models.ProductResponse, tags=["Products"])
async def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = product_crud.get_product_by_id(db=db, id=id)
    return product

@router.post("/products/", response_model=product_py_models.ProductResponse, tags=["Products"])
async def create_product(product: product_py_models.ProductRequest, db: Session = Depends(get_db)):
    db_product = product_crud.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name already exists")
    return product_crud.create_product(db, product_request=product)

@router.delete("/products/{id}", tags=["Products"])
async def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product doesn't exist!")
    return product_crud.delete_product(db=db, id=id)

@router.put("/products/{id}", response_model=product_py_models.ProductResponse, tags=["Products"])
async def edit_product_by_id(id: int, product: product_py_models.ProductRequest, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product doesn't exist!"
        )
    return product_crud.edit_product(db=db, id=id, product_request=product)