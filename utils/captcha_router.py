from fastapi import APIRouter
from utils.captcha import generate_captcha

router = APIRouter()
    
@router.get("/captcha")
def get_captcha():
    captcha_id, question = generate_captcha()
    return {"captcha_id": captcha_id, "question": question}
