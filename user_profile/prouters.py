from fastapi import APIRouter, Depends
from .schema import CreateProfile
from .service import create_profile, get_user_profile
from auth.auth import get_current_user
from user.models import User
from database.db import session

prouter = APIRouter()

@prouter.put("/updateprofile/")
def generate_profile(profile : CreateProfile,get_username: User = Depends(get_current_user)):
    return create_profile(profile,get_username)

@prouter.get("/profiledetails/")
def get_profile_details(current_user: User = Depends(get_current_user)):
    return get_user_profile(current_user.user_id)

