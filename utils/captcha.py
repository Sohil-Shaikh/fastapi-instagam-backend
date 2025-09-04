import random
import uuid

# In-memory CAPTCHA store (use Redis or DB in production)
captcha_store = {}

def generate_captcha():
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operator = random.choice(["+", "-"])
    
    if operator == "+":
        answer = num1 + num2
    else:
        answer = num1 - num2

    question = f"What is {num1} {operator} {num2} = ?"
    captcha_id = str(uuid.uuid4())[:6]
    captcha_store[captcha_id] = {
        "answer": str(answer),
        "attempts": 0,
        "question": question
    }

    return captcha_id, question
