from .schema import CreateUser
from database.db import Sessionlocal
from .models import User
from sqlalchemy import select
from fastapi import HTTPException, Depends
from user_profile.models import Profile
from auth.auth import create_access_token, verify_password, get_password_hash, verify_token, ACCEESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

# In-memory store for CAPTCHA answers
from utils.captcha import captcha_store

def create_user(register : CreateUser):

    captcha_data = captcha_store.get(register.captcha_id)

    if not captcha_data:
        raise HTTPException(status_code=400, detail="Invalid or expired CAPTCHA")

    # Check attempts
    if captcha_data["attempts"] >= 3:
        captcha_store.pop(register.captcha_id, None)
        raise HTTPException(
            status_code=400,
            detail="Too many attempts. Please get a new CAPTCHA."
        )

    # Check answer
    if register.captcha_answer.strip() != captcha_data["answer"]:
        captcha_data["attempts"] += 1
        raise HTTPException(status_code=400, detail="Incorrect CAPTCHA answer")

    # CAPTCHA is correct → clean it up
    captcha_store.pop(register.captcha_id)



    with Sessionlocal() as session:
        name = session.query(User).filter(User.username).all()
        emails = session.query(User.email).all()
        if register.username in name:
            raise HTTPException(status_code=409,detail="username already exist")
        if register.email in emails:
            raise HTTPException(status_code=409,detail="email already exist")
        user = User(username = register.username,email = register.email, password = get_password_hash(register.password))
        session.add(user)
        session.commit()
        n = session.query(User).where(User.username == register.username).first()
        profile = Profile(dob = "None",mobile= "None",gender="None",user_id = n.user_id)
        session.add(profile)
        session.commit()
        return {"msg":"user registered ;successfully","username": register.username}

def login_users(form_data: OAuth2PasswordRequestForm =Depends() ):
    with Sessionlocal() as session:
        user = session.query(User).filter(User.username==form_data.username).first()
        profile = session.query(Profile).filter(Profile.user_id == user.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="inavalid username")
        if not verify_password(form_data.password,user.password):
            raise HTTPException(status_code=404, detail="inavalid password")
        acces_token_expire = timedelta(minutes=ACCEESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub":user.username}
                                            ,expires_delta=acces_token_expire)
        return {'msg':'login successfully',"usename" : user.username ,"profile_id":profile.id,"access_token":access_token}


def change_password(new_password: str,token:str):
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401,detail="unauthorized user")
    with Sessionlocal() as session:
        user = session.query(User).filter(User.username==username).first()
        if not user:    
            raise HTTPException(status_code=404, detail="inavalid username")
        user.password = get_password_hash(new_password)
        session.commit()
        return {"msg":"password updated",username:new_password}


def get_users_data():
    with Sessionlocal() as session:
        stmt = select(User)
        data = session.scalars(stmt).all()
        return data

def delete_user(u_name:str,passw:str):
    with Sessionlocal() as session:
        user = session.query(User).filter(User.username == u_name).first()
        if not user:
            raise HTTPException(status_code=404,detail="username not exists")
        if user.password != get_password_hash(passw):
            raise HTTPException(status_code=404,detail="incorrect password")
        profile = session.query(Profile).filter(Profile.user_id == user.user_id).first()
        if profile:
            session.delete(profile)
        session.delete(user)
        session.commit()
        return {"msg":"user delete sucessfully"}



