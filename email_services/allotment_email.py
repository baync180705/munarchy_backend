import os
import aiosmtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

async def allotmentEmail(name, recieverEmail, committee, portfolio):
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    RECIEVER_EMAIL = recieverEmail
    subject = "Allotment for MUNARCHY'25"
    body = f"Dear {name}, Your allotment for MUNARCHY'25 is:\nCommittee:{committee}\nPortfolio:{portfolio}"

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