import os
import aiosmtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

async def registrationEmail(name, receiverEmail, munarchyId):
    load_dotenv()  # Ensure environment variables are loaded
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    EMAIL_SECRET_KEY = os.getenv("EMAIL_SECRET_KEY")

    subject = "Complete Your MUNarchy’25 Registration – Payment Pending | IIT Roorkee MUN"

    # HTML Email Body
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .header {{
                font-size: 1.2em;
                font-weight: bold;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 0.9em;
                color: #555;
            }}
        </style>
    </head>
    <body>
        <p class="header">Dear {name},</p>

        <p>Greetings from <strong>Team MUNarchy, IIT Roorkee!</strong></p>

        <p>You have completed the first step of registration for <strong>MUNarchy’25</strong>! Your <strong>MUNarchy ID</strong> for the event is <strong>{munarchyId}</strong>.</p>

        <p>
            You’ll require this ID to pay and complete the event registration! 
            Make a payment on the website to finalize your registration. 
            Keep this MUNarchy ID safe, as you will need it for portfolio allotment, 
            entry to IIT Roorkee’s campus, and general inquiries.
        </p>

        <p>We look forward to seeing you at <strong>MUNarchy’25</strong>!</p>

        <div class="footer">
            <p>Warm Regards,</p>
            <p><strong>Team MUNarchy</strong><br>
            IIT Roorkee Model United Nations<br>
            IIT Roorkee</p>
        </div>
    </body>
    </html>
    """

    # Plain Text Fallback
    plain_text_body = f"""
    Dear {name},

    Greetings from Team MUNarchy, IIT Roorkee!

    You have completed the first step of registration for MUNarchy’25! Your MUNarchy ID for the event is {munarchyId}.
    You’ll require this ID to pay and complete the event registration! 
    Make a payment on the website to finalize your registration. 
    Keep this MUNarchy ID safe, as you will need it for portfolio allotment, entry to IIT Roorkee’s campus, and general inquiries.

    We look forward to seeing you at MUNarchy’25!

    Warm Regards,
    Team MUNarchy
    IIT Roorkee Model United Nations
    IIT Roorkee
    """

    # Create a MIME message
    message = MIMEMultipart("alternative")
    message["From"] = SENDER_EMAIL
    message["To"] = receiverEmail
    message["Subject"] = subject

    # Attach both plain text and HTML versions
    message.attach(MIMEText(plain_text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    # Send the email using aiosmtplib
    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        username=SENDER_EMAIL,
        password=EMAIL_SECRET_KEY,
        start_tls=True,
    )