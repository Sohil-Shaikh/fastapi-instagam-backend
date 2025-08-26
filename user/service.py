from .schema import CreateUser
from database.db import Sessionlocal
from .models import User
from sqlalchemy import select
from fastapi import HTTPException
from user_profile.models import Profile
# from passlib.hash import bcrypt

def create_user(register : CreateUser):
    with Sessionlocal() as session:
        stmt = select(User.username)
        name = session.scalars(stmt).all()
        # name = session.query(User).filter(User.username).all()
        stmt2 = select(User.email)
        emails= session.scalars(stmt2).all()
        if register.username in name:
            raise HTTPException(status_code=409,detail="username already exist")
        if register.email in emails:
            raise HTTPException(status_code=409,detail="email already exist")
        user = User(username = register.username,email = register.email, password = register.password)
        session.add(user)
        session.commit()
        st = select(User).where(User.username == register.username)
        name = session.scalars(st).first()
        profile = Profile(dob = "None",mobile= "None",gender="None",user_id = name.user_id)
        session.add(profile)
        session.commit()
        return {"msg":"user registered ;successfully","username": register.username}

def login_users(username:str,password:str):
    with Sessionlocal() as session:
        stmt = select(User).where(User.username==username)
        user = session.scalars(stmt).first()
        if not user:
            raise HTTPException(status_code=404, detail="inavalid username")
        if user.password != password:
            raise HTTPException(status_code=404, detail="inavalid password")
        return {'msg':'login successfully',"usename" : username}


def change_password(uname:str,passw:str,new_password:str):
    with Sessionlocal() as session:
        stmt = select(User).where(User.username==uname)
        user = session.scalars(stmt).first()
        if not user:
            raise HTTPException(status_code=404, detail="inavalid username")
        if user.password != passw:
            raise HTTPException(status_code=404, detail="inavalid password")
        user.password = new_password
        session.commit()
        return {"msg":"password updated",uname:new_password}


def get_users_data():
    with Sessionlocal() as session:
        stmt = select(User)
        data = session.scalars(stmt).all()
        return data

def delete_user(u_name:str,passw:str):
    with Sessionlocal() as session:
        stmt = select(User).where(User.username == u_name)
        user = session.scalars(stmt).first()
        if not user:
            raise HTTPException(status_code=404,detail="username not exists")
        if user.password != passw:
            raise HTTPException(status_code=404,detail="incorrect password")
        st = select(Profile).where(Profile.user_id == user.user_id)
        profile = session.scalars(st).first()
        if profile:
            session.delete(profile)
        session.delete(user)
        session.commit()
        return {"msg":"user delete sucessfully"}