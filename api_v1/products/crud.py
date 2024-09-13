from sqlalchemy import Select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from .shemas import ProductCreate


async def get_products(session: AsyncSession) -> list[Product]:
    stat = Select(Product).order_by(Product.id)
    result: Result = await session.execute(stat)
    products = result.scalars().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, new_product: ProductCreate) -> Product:
    product = Product(**new_product.model_dump())
    session.add(product)
    await session.commit()
    # await session.refresh(product)
    return product
