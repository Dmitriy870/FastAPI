"""
Create
Read
Update
Delete
"""
from users.shemas import Create_user


def create_user(user_in:Create_user):
     user = user_in.model_dump()
     return {
         "success": True,
         "user": user,
     }



