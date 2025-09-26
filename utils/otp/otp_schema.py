from pydantic import BaseModel
class OTPVerifyRequest(BaseModel):
    username: str
    otp: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str