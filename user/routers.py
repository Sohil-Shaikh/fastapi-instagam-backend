from fastapi import APIRouter
from .schema import CreateUser
from .service import create_user,login_users, change_password, get_users_data, delete_user

router = APIRouter()

@router.post("/register/")
def regiser_user(register : CreateUser):
    return create_user(register)

@router.post("/login/")
def login_user(username:str,password:str):
    return login_users(username,password)

@router.put("/changepas/")
def change_pas(username:str,passw:str,new_password:str):
    return change_password(username,passw,new_password)


@router.get("/get/")
def get_data():
    return get_users_data()


@router.delete("/delete/")
def delete_users(u_name:str,passw:str):
    return delete_user(u_name,passw)