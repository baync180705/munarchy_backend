import os
import aiosmtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

async def registrationEmail(name, recieverEmail, munarchyId):
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    RECIEVER_EMAIL = recieverEmail
    subject = "Complete Your MUNarchy’25 Registration – Payment Pending | IIT Roorkee MUN"
    body = f'''
    Dear {name},

    Greetings from Team MUNarchy, IIT Roorkee!

    You have completed the first step of registration for MUNarchy’25!! Your MUNarchy ID for the event is {munarchyId}.
    You’ll require this ID to pay and complete the event registration! Make a payment on the website to complete your registration. 
    Keep this MUNarchy ID safe, as you would need this to check portfolio allotment, entry to IIT Roorkee’s campus, and general enquiries

    We look forward to seeing you at MUNarchy’25!. 

    Warm Regards
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