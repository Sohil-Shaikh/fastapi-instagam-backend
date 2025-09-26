from fastapi import APIRouter,Depends
from .schema import CreateUser
from .service import create_user,login_users, change_password, delete_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(prefix="/user")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login/")


@router.post("/register/")
def regiser_user(register : CreateUser):
    return create_user(register)

# @router.post("/login/")
# def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
#     return login_users(form_data)

@router.put("/changepas/")
def change_pas(new_password:str, token: str = Depends(oauth2_scheme)):
    return change_password(new_password,token)


@router.delete("/delete/")
def delete_users(u_name:str,passw:str):
    return delete_user(u_name,passw)

