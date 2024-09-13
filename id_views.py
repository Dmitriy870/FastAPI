from random import randint
from typing import Annotated

from fastapi import Path, APIRouter

router = APIRouter(prefix= '/id',tags=["id"])


@router.get("/random_id")
async def rand_id():
    return {"Your id:": randint(1, 100)}

@router.get ("/")
async def id (id_code :Annotated[int,Path(ge=1)]):
    return {"Your id:": id_code}