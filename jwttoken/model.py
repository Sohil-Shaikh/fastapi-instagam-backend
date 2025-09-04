from jwttoken.db import Base
from sqlalchemy import Column, String, Boolean



class Users(Base):
    __tablename__ = "usertable"
    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    def __repr__(self):
        return f"username = {self.username} password = {self.password}"
    

class Application(Base):
    __tablename__ = "devices"
    device_name = Column(String(50))
    
