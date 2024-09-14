from fastapi import APIRouter, Depends
from starlette import status

from core.models import db_helper
from . import crud
from .dependencies import product_by_id
from .shemas import ProductCreate, Product, ProductUpdate, ProductPartialUpdate

router = APIRouter(tags=["products"])
from sqlalchemy.ext.asyncio import AsyncSession


@router.get("/", response_model=list[Product])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_products(session=session)


@router.get("/{product_id}/", response_model=Product)
async def get_product(
    product: Product = Depends(product_by_id),
):
    return product


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(session, product_in)


@router.put("/{product_id}/", response_model=Product)
async def update_product(
    product_update: ProductUpdate,
    product=Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session, product=product, product_update=product_update
    )


@router.patch("/{product_id}/", response_model=Product)
async def update_product(
    product_update: ProductPartialUpdate,
    product=Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session, product=product, product_update=product_update, partial=True
    )


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    product=Depends(product_by_id),
):
    return await crud.delete_product(session, product)
