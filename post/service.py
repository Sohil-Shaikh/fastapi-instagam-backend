from fastapi import HTTPException
from .models import UserPosts
from .schema import CreatePost
from database.db import session
from user.models import User

def create_post(schema: CreatePost,current_user: str):
    user = session.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404,detail="user not exists")
    postdetails = UserPosts(post_name = schema.post_name,image = schema.image,description = schema.description,u_id = user.user_id )
    session.add(postdetails)
    session.commit()
    return {"msg":"post successfully created"}


def get_posts(current_user: str):
    user = session.query(User).filter(User.username==current_user.username).first()
    if not user:
        raise HTTPException(status_code=404,detail="user not exists")
    posts = session.query(UserPosts).filter(UserPosts.u_id == user.user_id).all()
    return posts

def update_post(current_user,id,new_description):
    user = session.query(User).filter(User.username == current_user.username).first()
    if not user:
        raise HTTPException(status_code=404,detail="username not exists")
    
    p = session.query(UserPosts).filter(UserPosts.post_id == id).first()
    if not p:
        raise HTTPException(status_code=404,detail='post not found')
    p.description = new_description
    session.commit()
    return {"msg":"post details updated","post":p}


def del_post(current_user : str,id:int): 
    user = session.query(User).filter(User.username == current_user.username).first()
    posts = session.query(UserPosts).filter(UserPosts.post_id == id).first()
    if not user:
        raise HTTPException(status_code=404,detail="username not exists")
    if not posts:
        raise HTTPException(status_code=404,detail="post not found")
    session.delete(posts)
    session.commit()
    return {'msg':"post seccessfully deleted"}

    