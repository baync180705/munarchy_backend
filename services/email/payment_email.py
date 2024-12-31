import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.settings import Settings

settings = Settings()

async def paymentEmail(name, receiverEmail):
    subject = "Payment Confirmation for MUNarchy'25 | IIT Roorkee MUN"

    html_body = f'''
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
                }}
                .header {{
                    text-align: center;
                    color: #0d47a1;
                    margin-bottom: 20px;
                }}
                .header h1 {{
                    font-size: 22px;
                    margin: 0;
                }}
                .header p {{
                    font-size: 16px;
                    margin: 5px 0 0;
                }}
                .content {{
                    font-size: 16px;
                    color: #555555;
                    line-height: 1.6;
                }}
                .highlight {{
                    color: #0d47a1;
                    font-weight: bold;
                }}
                .instructions {{
                    margin: 20px 0;
                    padding: 15px;
                    background-color: #e3f2fd;
                    border: 1px solid #0d47a1;
                    border-radius: 5px;
                    font-size: 15px;
                }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    font-size: 14px;
                    color: #777777;
                }}
                .contact {{
                    margin: 10px 0;
                    font-size: 16px;
                    color: #555555;
                }}
                .contact span {{
                    font-weight: bold;
                }}
                .button-container {{
                    text-align: center;
                    margin: 20px 0;
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
            </style>
        </head>
        <body>
            <div class="container">
                <!-- Header -->
                <div class="header">
                    <h1>Registration Confirmed!</h1>
                    <p>Welcome to MUNarchy’25</p>
                </div>

                <!-- Content -->
                <div class="content">
                    <p>Dear <span class="highlight">{name}</span>,</p>
                    <p>Congratulations! Your payment for <span class="highlight">MUNarchy’25</span> has been successfully processed.</p>
                </div>

            <!-- What’s Next Section -->
        <div class="instructions">
            <h3 style="text-align: center; color: #0d47a1; font-size: 18px; margin-bottom: 10px;">What’s Next?</h3>
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li style="margin-bottom: 15px;">
                    <strong style="color: #1a237e;">Portfolio Allotment:</strong> 
                    Your allotted portfolio will be sent to your registered email soon. You can also check it on our website after the allotments are done: 
                    <a href="https://irmun.iitr.ac.in" target="_blank" style="color: #0d47a1; text-decoration: none;">irmun.iitr.ac.in</a>.
                </li>
                <li>
                    <strong style="color: #1a237e;">Conference Details:</strong> 
                    Watch your email for updates and further instructions. Please ensure your contact information is correct to avoid missing out!
                </li>
            </ul>
        </div>


                <!-- Exciting Statement -->
                <div class="content">
                    <p>We are excited to welcome you to IIT Roorkee’s first fully-fledged MUN conference. Get ready to experience an engaging and unforgettable journey at MUNarchy’25!</p>
                </div>

                <!-- Contact Section -->
                <div class="contact">
                    <p>Have Questions?</p>
                    <p>For any queries regarding the conference, feel free to contact:</p>
                    <p><span>Sumedh:</span> +91 98506 72970</p>
                </div>

                <!-- Button -->
                <div class="button-container">
                    <a class="button" href="https://irmun.iitr.ac.in" target="_blank">Visit Website</a>
                </div>

                <!-- Footer -->
                <div class="footer">
                    <p>Warm regards,<br>Team MUNarchy</p>
                    <p>IIT Roorkee Model United Nations<br>IIT Roorkee</p>
                </div>
            </div>
        </body>
        </html>
    ''' 

    plain_text_body = f'''
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