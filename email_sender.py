import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

def send_email(to_email, subject, body):
    
    response = resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": [to_email],
        "subject": subject,
        "text": body
    })
    
    return response