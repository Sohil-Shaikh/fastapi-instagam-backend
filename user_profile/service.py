from database.db import session
from .schema import CreateProfile
from sqlalchemy import select
from .models import Profile
from user.models import User
from fastapi import HTTPException


def create_profile(username:str, password:str, profile = CreateProfile):
    # st = select(User).where(User.username == username)
    # user = session.scalars(st).first()
    user = session.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(status_code=404,detail="user not exists")
    if user.password != password:
        raise HTTPException(status_code=404,detail="incorrect password")
    st1 = select(Profile).where(Profile.user_id == user.user_id)
    prof = session.scalars(st1).first()
    prof.dob = profile.dob or prof.dob
    prof.mobile = profile.mobile or prof.mobile
    prof.gender = profile.gender or prof.gender
    session.commit()
    return {'msg':"data updated"}

def get_user_profile(profile_id:int):
    st1 = select(Profile.id)
    prof_id = session.scalars(st1).all()
    if profile_id not in prof_id:
        raise HTTPException(status_code=404,detail="profile not found, enter correct id")
    stmt = select(Profile).where(Profile.id  == profile_id)
    profile = session.scalars(stmt).first()
    st = select(User).where(User.user_id == profile.user_id )
    user = session.scalars(st).first()
    return {"user":user,"profile":profile}

 