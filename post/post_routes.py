from fastapi import APIRouter
from .schema import CreatePost
from .service import create_post, get_posts, update_post, del_post

postrouter = APIRouter()

@postrouter.post("/createpost/")
def create_your_post(username:str,password:str,schema : CreatePost):
    return create_post(username, password,schema)

@postrouter.get('/getallposts/')
def get_users_posts(username:str,password:str):
    return get_posts(username,password)


@postrouter.put("/updatepost/")
def edit_post(id:int,desc:str):
    return update_post(id,desc)


@postrouter.delete("/delelepost/")
def delete_post(username:str,password:str,post_id:int):
    return del_post(username,password,post_id)
