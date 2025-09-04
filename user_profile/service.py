from database.db import session
from .schema import CreateProfile
from sqlalchemy import select
from .models import Profile
from user.models import User
from fastapi import HTTPException, Depends
from post.models import UserPosts
from auth.auth import get_current_user


def create_profile(profile = CreateProfile, get_username: User = Depends(get_current_user),):
    prof = session.query(Profile).filter(Profile.user_id == get_username.user_id).first()
    if not prof:
        raise HTTPException(status_code=404,detail="profile not found")
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
    user = session.query(User).where(User.user_id == profile.user_id ).first()
    posts = session.query(UserPosts).filter(UserPosts.u_id == user.user_id).count()
    return {"user":user,"profile":profile,"number of post":posts}

