from ensurepip import version
from fastapi import APIRouter
from service.routers import api_router_product, api_router_order





routers = APIRouter()



routers.include_router(api_router_product.router, prefix="/api/v1")
routers.include_router(api_router_order.router, prefix="/api/v1")
