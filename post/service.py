from fastapi import HTTPException
from .models import UserPosts
from .schema import CreatePost
from database.db import session
from user.models import User

def create_post(username:str,password:str,schema: CreatePost):
    user = session.query(User).where(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404,detail="user not exists")
    print(user)
    if user.password != password:
        raise HTTPException(status_code=404,detail="incorrect password")
    postdetails = UserPosts(post_name = schema.post_name,image = schema.image,description = schema.description,u_id = user.user_id )
    session.add(postdetails)
    session.commit()
    return {"msg":"post successfully created"}


def get_posts(username:str, password:str):
    user = session.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(status_code=404,detail="user not exists")
    if user.password != password:
        raise HTTPException(status_code=404,detail="incorrect password")
    posts = session.query(UserPosts).filter(UserPosts.u_id == user.user_id).all()
    return posts

def update_post(id,new_description):
    p = session.query(UserPosts).filter(UserPosts.post_id == id).first()
    if not p:
        raise HTTPException(status_code=404,detail='post not found')
    p.description = new_description
    session.commit()
    return {"msg":"post details updated","post":p}

def del_post(username:str,password:str,id:int): 
    user = session.query(User).filter(User.username == username).first()
    posts = session.query(UserPosts).filter(UserPosts.post_id == id).first()
    if not user:
        raise HTTPException(status_code=404,detail="username not exists")
    if user.password != password:
        raise HTTPException(status_cod=404, detail="incorrect password")
    if not posts:
        raise HTTPException(status_code=404,detail="post not found")
    session.delete(posts)
    session.commit()
    return {'msg':"post seccessfully deleted"}
    

    