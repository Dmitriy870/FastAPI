import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

from id_views import router as id_router
from users.views import router as users_router


app = FastAPI()

app.include_router(id_router)
app.include_router(users_router)


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
