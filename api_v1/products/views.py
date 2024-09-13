from fastapi import APIRouter
from . import crud
from .shemas import ProductCreate, Product

router = APIRouter(tags=["products"])


@router.get("/", response_model=list[Product])
async def get_prod(session):
    return await crud.get_products(session)


@router.get("/find_poduct_id", response_model=Product)
async def find_product_id(session, product_id: int):
    return await crud.get_product(session, product_id)


@router.post("/create", response_model=Product)
async def create_product(session, new_prod: ProductCreate):
    return await crud.create_product(session, new_prod)
