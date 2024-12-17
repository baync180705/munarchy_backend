import os
import aiosmtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

async def paymentEmail(name, recieverEmail, net_amount_debit, accomodation):
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    RECIEVER_EMAIL = recieverEmail
    subject = "Registration Confirmed – Welcome to MUNarchy’25!"
    body = f'''
    Dear {name},

    Congratulations! Your payment for MUNarchy’25 has been successfully processed | IIT Roorkee MUN

    What’s Next?
    Portfolio Allotment: Your allotted portfolio will be sent to your registered email soon. You can also check it on our website after the allotments are done: irmun.iitr.ac.in.
    Conference Details: Watch your email for updates and further instructions.


    Have Questions?
    For any queries regarding the conference, feel free to contact:
    Sumedh: +91 98506 72970

    We are excited to welcome you to IIT Roorkee’s first fully-fledged MUN conference. Get ready to experience an engaging and unforgettable journey at MUNarchy’25!

    Thank you for joining us. See you soon!

    Warm regards,
    Team MUNarchy
    IIT Roorkee Model United Nations
    IIT Roorkee
    '''

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