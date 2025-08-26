from pydantic import BaseModel
from sqlalchemy import Date

class CreateProfile(BaseModel):
    dob : str
    mobile : int
    gender : str
    
