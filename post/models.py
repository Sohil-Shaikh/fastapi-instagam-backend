from sqlalchemy import Column, Integer, String, BLOB, ForeignKey
from sqlalchemy.orm import relationship
from user.models import User
from database.db import Base


class UserPosts(Base):
    __tablename__="userposts"
    post_id = Column(Integer,primary_key=True)
    post_name = Column(String)
    image = Column(BLOB)
    description = Column(String,nullable=True)
    u_id = Column(Integer,ForeignKey("users.user_id"))

    user = relationship("User", back_populates="posts")


    def __repr__(self):
        return f"post_id = {self.post_id} post_name = {self.post_name} image = {self.image} description = {self.description} user_id = {self.u_id}"
    