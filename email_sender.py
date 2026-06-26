import os
import resend
from dotenv import load_dotenv

load_dotenv()

def send_email(to_email, subject, body):
    resend.api_key = os.getenv("RESEND_API_KEY")
    
    response = resend.emails.send({
        "from": "onboarding@resend.dev",
        "to": [to_email],
        "subject": subject,
        "text": body
    })
    
    return response