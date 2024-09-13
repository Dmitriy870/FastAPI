from fastapi import APIRouter
from users.shemas import Create_user
from users import crud

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/user")
def create_user(user: Create_user):
    return crud.create_user(user)
