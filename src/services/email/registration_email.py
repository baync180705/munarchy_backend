import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.settings import Settings

settings = Settings()

async def registrationEmail(name, receiverEmail, munarchyId):
    subject = "Complete Your MUNarchy’25 Registration – Payment Pending | IIT Roorkee MUN"

    html_body = f"""
    <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f7f7f7;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }}
                .header {{
                    font-size: 18px;
                    color: #333333;
                    margin-top: 10px;
                }}
                .mun-id-box {{
                    margin: 20px 0;
                    text-align: center;
                    padding: 15px;
                    border: 2px dashed #0d47a1;
                    border-radius: 5px;
                    font-size: 22px;
                    font-weight: bold;
                    color: #0d47a1;
                }}
                .copy-box {{
                    margin: 20px auto;
                    text-align: center;
                    padding: 15px;
                    background-color: #283593;
                    border: 2px solid #1a237e;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 18px;
                    color: #ffffff;
                    font-weight: bold;
                    max-width: 300px;
                }}
                .copy-box:hover {{
                    background-color: #1a237e;
                }}
                .button-container {{
                    text-align: center;
                    margin-top: 20px;
                }}
                .button {{
                    display: inline-block;
                    text-decoration: none;
                    padding: 12px 25px;
                    background-color: #1a237e;
                    color: #ffffff;
                    border-radius: 5px;
                    font-size: 16px;
                    font-weight: bold;
                }}
                .button:hover {{
                    background-color: #0d47a1;
                }}
                .instructions {{
                    margin-top: 20px;
                    font-size: 16px;
                    color: #555555;
                    line-height: 1.5;
                }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    font-size: 14px;
                    color: #777777;
                }}

                /* Media Queries for Responsiveness */
                @media (max-width: 600px) {{
                    .container {{
                        padding: 15px;
                    }}
                    .mun-id-box, .copy-box {{
                        font-size: 20px;
                        padding: 10px;
                    }}
                    .button {{
                        padding: 10px 20px;
                        font-size: 14px;
                    }}
                }}

                @media (max-width: 400px) {{
                    .mun-id-box, .copy-box {{
                        font-size: 18px;
                    }}
                    .button {{
                        padding: 8px 15px;
                        font-size: 12px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">

                <div class="header">
                    <p>Dear {name}!</p>
                    <p>Greetings from Team MUNarchy, IIT Roorkee!</p>
                    <p>Complete Your Registration for MUNarchy’25</p>
                </div>

                <div class="mun-id-box" id="mun-id">
                    {munarchyId}
                </div>

                <div class="instructions">
                    <p>You’ll require this ID to pay and complete the event registration!</p>
                    <p>Make a payment on the website to finalize your registration. Keep this MUNarchy ID safe, as you will need it for:</p>
                    <ul>
                        <li>Portfolio allotment</li>
                        <li>Entry to IIT Roorkee’s campus</li>
                        <li>General inquiries</li>
                    </ul>
                </div>

                <div class="button-container">
                    <a class="button" href="https://irmun.iitr.ac.in/payment" target="_blank">Complete Payment</a>
                </div>

                <div class="footer">
                    <p>We look forward to seeing you at MUNarchy’25!</p>
                    <p>Warm Regards,<br>Team MUNarchy</p>
                </div>
            </div>
        </body>
        </html>
    """
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
    message = MIMEMultipart("alternative")
    message["From"] = settings.SENDER_EMAIL
    message["To"] = receiverEmail
    message["Subject"] = subject

    message.attach(MIMEText(plain_text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        username=settings.SENDER_EMAIL,
        password=settings.EMAIL_SECRET_KEY,
        start_tls=True,
    ) 