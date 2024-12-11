import os
import aiosmtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

async def registrationEmail(name, recieverEmail, munarchyId):
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    RECIEVER_EMAIL = recieverEmail
    subject = "Your MUNARCHY ID has been successfully generated"
    body = f"Dear {name}, your MUNARCHY ID is {munarchyId}. Happy munning !"

    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = RECIEVER_EMAIL
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        username=SENDER_EMAIL,
        password=os.getenv("EMAIL_SECRET_KEY"),
        start_tls=True,
    )