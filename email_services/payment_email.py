import os
import aiosmtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

async def paymentEmail(name, recieverEmail, net_amount_debit, accomodation):
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    RECIEVER_EMAIL = recieverEmail
    EMAIL_SECRET_KEY = os.getenv("EMAIL_SECRET_KEY")
    subject = "Registration Confirmed – Welcome to MUNarchy’25!"

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
                .logo-container {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .logo {{
                    width: 100px;
                    height: auto;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <!-- Logo Section -->
                <div class="logo-container">
                    <img src="data:image/png;base64, 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" alt="MUNarchy Logo" class="logo">
                </div>

                <!-- Header -->
                <div class="header">
                    <h1>Registration Confirmed!</h1>
                    <p>Welcome to MUNarchy’25</p>
                </div>

                <!-- Content -->
                <div class="content">
                    <p>Dear <span class="highlight">Manmath</span>,</p>
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
    message["From"] = SENDER_EMAIL
    message["To"] = receiverEmail
    message["Subject"] = subject

    message.attach(MIMEText(plain_text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        username=SENDER_EMAIL,
        password=EMAIL_SECRET_KEY,
        start_tls=True,
    )