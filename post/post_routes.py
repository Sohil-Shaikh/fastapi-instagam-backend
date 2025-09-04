from fastapi import APIRouter, Depends
from .schema import CreatePost
from .service import create_post, get_posts, update_post, del_post
from auth.auth import get_current_user
from user.models import User

postrouter = APIRouter()

@postrouter.post("/createpost/")
def create_your_post(schema : CreatePost, current_user: User = Depends(get_current_user)):
    return create_post(schema,current_user.username)


@postrouter.get('/getallposts/')
def get_users_posts(current_user: User = Depends(get_current_user)):
    return get_posts(current_user)


@postrouter.patch("/updatepost/")
def edit_post(id:int,desc:str,current_user: User = Depends(get_current_user)):
    return update_post(current_user,id,desc)


@postrouter.delete("/delelepost/")
def delete_post(post_id:int,current_user: User = Depends(get_current_user)):
    return del_post(current_user,post_id)
