from sqlalchemy import Column, String, Integer, Date,ForeignKey
from database.db import Base
from sqlalchemy.orm import relationship
from user.models import User

class Profile(Base):
    __tablename__ ="profiles"
    id = Column(Integer,primary_key=True)
    dob = Column(String(10))
    mobile = Column(String(15))
    gender = Column(String(20),nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True)

    user = relationship('User', back_populates='profile')

    def __repr__(self):
        return f'id = {self.id} DOB = {self.dob} mobile = {self.mobile} user_id = {self.user_id}'
