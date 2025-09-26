from sqlalchemy import Column,Integer, String, DateTime
from datetime import datetime
from database.db import Base
class OTP(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    otp = Column(String)
    expires_at = Column(DateTime, default=datetime.utcnow)


