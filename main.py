from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1 import router as api_v1_router
from core.config import settings
from core.models import Base, db_helper
from id_views import router as id_router
from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(id_router)
app.include_router(users_router)
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
