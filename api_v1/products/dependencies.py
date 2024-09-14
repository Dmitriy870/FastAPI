from pathlib import Path
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .crud import get_product


async def product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    prod = await get_product(session, product_id)
    if prod is not None:
        return prod
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
