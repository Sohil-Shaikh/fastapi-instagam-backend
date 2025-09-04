from pydantic import BaseModel

class CreateUser(BaseModel):
    username : str
    email : str
    password :str

    # for captcha
    captcha_id: str
    captcha_answer: str

class Auth(BaseModel):
    username : str
    password :str