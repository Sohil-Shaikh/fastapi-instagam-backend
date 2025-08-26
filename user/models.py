from sqlalchemy import Column, String, Integer
from database.db import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__="users"
    user_id = Column(Integer,primary_key=True)
    username = Column(String(50),nullable=False,unique=True)
    email = Column(String,nullable=False)
    password = Column(String(50),nullable=False)

    profile = relationship('Profile', back_populates='user', uselist=False)
    posts = relationship("UserPosts", back_populates="user", cascade="all, delete-orphan")
    def __repr__(self):
        return f"<User user_id={self.user_id}\n username={self.username}\n email = {self.email}\n password={self.password} >"
    
    