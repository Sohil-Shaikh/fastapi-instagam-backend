from fastapi import FastAPI
from user_profile.models import Profile
from user.models import User
from post.post_routes import postrouter
from user.routers import router
from user_profile.prouters import prouter
from database.db import engine, Base
from utils.captcha_router import router as captcha_router
from utils.otp.otprouter import router as otprouter

app =  FastAPI()

app.include_router(captcha_router,tags=["CAPTCHA ROUTES"])
app.include_router(router,tags=["USER ROUTES"])
app.include_router(otprouter,tags=["otprouter"])
app.include_router(prouter,tags=["PROFILE ROUTES"])
app.include_router(postrouter,tags=["POST ROUTES"])
app.include_router(otprouter,tags=["otprouter"])

Base.metadata.create_all(engine)