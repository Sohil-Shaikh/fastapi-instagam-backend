from fastapi import FastAPI
from user_profile.models import Profile
from user.models import User
from post.post_routes import postrouter
from user.routers import router
from user_profile.prouters import prouter
from database.db import engine, Base

app =  FastAPI()

app.include_router(router,tags=["USER ROUTES"])
app.include_router(prouter,tags=["PROFILE ROUTES"])
app.include_router(postrouter,tags=["POST ROUTES"])


Base.metadata.create_all(engine)