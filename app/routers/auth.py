from fastapi import APIRouter
import math
import random
import smtplib
from email.message import EmailMessage
from ..config import setting

router = APIRouter(tags=["Authentication"]) 


def send_otp(id: str):
    num = "0123456789"
    val = ""
    for _ in range(0, 6):
        val += num[math.floor(random.random()*10)]

    msg = EmailMessage()
    OTP = "Please Verify your OTP |"+" "+val + " is your OTP."
    msg['subject'] = "OTP VERIFICATION"
    msg['From'] = "Mr.Wash"
    msg['To'] = id
    msg.set_content(OTP)
    message = msg
    email = smtplib.SMTP('smtp.gmail.com', 587)
    email.starttls()
    email.login(setting.SENDER_EMAIL, setting.SENDER_EMAIL_APP_PASSWORD)
    email.send_message(message)
    del msg["To"]
    return val
    
    

