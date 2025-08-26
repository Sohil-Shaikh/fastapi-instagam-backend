from fastapi import APIRouter
from .schema import CreateProfile
from .service import create_profile, get_user_profile

prouter = APIRouter()

@prouter.put("/updateprofile/")
def generate_profile(username:str, password:str,profile : CreateProfile):
    return create_profile(username, password, profile)

@prouter.get("/profiledetails/")
def get_profile_details(profile_id:int):
    return get_user_profile(profile_id)
