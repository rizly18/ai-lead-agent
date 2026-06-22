import os
from resend import Resend
from dotenv import load_dotenv

load_dotenv()

client = Resend(api_key=os.getenv("RESEND_API_KEY"))

def send_email(to_email, subject, body):

    client.emails.send({
        "from": "onboarding@resend.dev",
        "to": [to_email],
        "subject": subject,
        "text": body
    })