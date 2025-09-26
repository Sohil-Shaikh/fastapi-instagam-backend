from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from database.db import Sessionlocal
from user.models import User
from user_profile.models import Profile
from utils.otp.otp_model import OTP
from utils.otp.otp_schema import LoginRequest, OTPVerifyRequest, TokenResponse
from auth import auth

router = APIRouter()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

# Step 1: Login → generate OTP
@router.post("/login")
def login_user(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid username")

    if not auth.verify_password(req.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid password")

    # generate OTP
    otp = str(random.randint(100000, 999999))
    expiry = datetime.utcnow() + timedelta(minutes=5)

    # save OTP
    db_otp = OTP(username=user.username, otp=otp, expires_at=expiry)
    db.add(db_otp)
    db.commit()

    # TODO: send OTP via email/SMS
    print(f"DEBUG: OTP for {user.username} is {otp}")

    return {"msg": "OTP sent to your registered email/phone"}

# Step 2: Verify OTP → return JWT
@router.post("/verify-otp", response_model=TokenResponse)
def verify_otp(req: OTPVerifyRequest, db: Session = Depends(get_db)):
    otp_record = (
        db.query(OTP)
        .filter(OTP.username == req.username)
        .order_by(OTP.expires_at.desc())
        .first()
    )

    if not otp_record:
        raise HTTPException(status_code=400, detail="OTP not requested")

    if datetime.utcnow() > otp_record.expires_at:
        raise HTTPException(status_code=400, detail="OTP expired")

    if otp_record.otp != req.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # OTP valid → issue JWT
    access_token_expires = timedelta(minutes=auth.ACCEESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": req.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
