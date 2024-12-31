import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.settings import Settings

settings = Settings()

async def allotmentEmail(name, receiverEmail, committee, portfolio):
    subject = "Portfolio Allotment for MUNarchy'25 | IIT Roorkee MUN"

    message = MIMEMultipart()
    message['From'] = settings.SENDER_EMAIL
    message['To'] = receiverEmail
    message['Subject'] = subject

    body = f"""Dear {name},
    Your portfolio for MUNarchy'25 has been allotted:
    Committee: {committee}
    Portfolio: {portfolio}

    Best regards,
    Team MUNarchy"""

    message.attach(MIMEText(body, 'plain'))

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        username=settings.SENDER_EMAIL,
        password=settings.EMAIL_SECRET_KEY,
        start_tls=True,
    ) 