from fastapi import APIRouter, HTTPException, status, Depends
from . import crud
from .shemas import ProductCreate, Product
from core.models import db_helper

router = APIRouter(tags=["products"])
from sqlalchemy.ext.asyncio import AsyncSession


@router.get("/", response_model=list[Product])
async def get_prod(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_products(session)


@router.get("/find_poduct_id", response_model=Product)
async def find_product_id(
    product_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_product(session, product_id)


@router.post("/create", response_model=Product)
async def create_product(
    new_prod: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    prod = await crud.create_product(session, new_prod)
    if prod is not None:
        return prod
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
