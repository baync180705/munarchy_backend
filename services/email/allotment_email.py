import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.settings import Settings

settings = Settings()

async def allotmentEmail(name, receiverEmail, committee, portfolio):
    subject = "Portfolio Allotment for MUNarchy 2025"

    html_body = f'''
            <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Portfolio Allotment - MUNarchy 2025</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 0;
                    background-color: #f8f9fa;
                    color: #333;
                }}
                .container {{
                    width: 100%;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .header h1 {{
                    font-size: 24px;
                    margin: 0;
                    color: #4CAF50;
                }}
                .content {{
                    margin-bottom: 20px;
                }}
                .content p {{
                    margin: 10px 0;
                }}
                .content .details {{
                    margin: 20px 0;
                    padding: 10px;
                    background-color: #f1f1f1;
                    border-left: 4px solid #4CAF50;
                }}
                .contact {{
                    margin-top: 20px;
                }}
                .contact p {{
                    margin: 5px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    font-size: 14px;
                    color: #555;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>MUNarchy 2025</h1>
                </div>

                <div class="content">
                    <p>Dear {name},</p>

                    <p>Greetings from the Secretariat of MUNarchy 2025!</p>

                    <p>We sincerely thank you for registering for the inaugural edition of IIT Roorkee's Model United Nations conference, scheduled to take place from <strong>17th to 19th January 2025</strong>. Your enthusiasm and commitment to being a part of this event mean a lot to us.</p>

                    <p>After a thorough selection process, we are delighted to inform you that a portfolio has been allotted to you. Please find the details below:</p>

                    <div class="details">
                        <p><strong>Committee:</strong> {committee}</p>
                        <p><strong>Portfolio:</strong> {portfolio}</p>
                    </div>

                    <p>For any queries or assistance, feel free to reach out to:</p>

                    <div class="contact">
                        <p><strong>Janhavi:</strong> +91 9021774682</p>
                        <p><strong>Kanav:</strong> +91 9971356475</p>
                        <p>Or write to us at <a href="mailto:irmun@iitr.ac.in">irmun@iitr.ac.in</a></p>
                    </div>

                    <p>We look forward to your meaningful contributions to MUNarchy 2025 and are excited to welcome you to this platform of dialogue and diplomacy.</p>
                </div>

                <div class="footer">
                    <p><strong>The Secretariat</strong><br>
                    MUNarchy 2025<br>
                    IIT Roorkee Model United Nations<br>
                    <a href="https://instagram.com/ir_mun.s" target="_blank">Instagram: ir_mun.s</a>
                    </p>

                    <p><em>"The Reign of Diplomacy"</em></p>
                </div>
            </div>
        </body>
        </html>
    '''

    plain_text_body = f"""
        MUNarchy 2025

        Dear {name},

        Greetings from the Secretariat of MUNarchy 2025!

        We sincerely thank you for registering for the inaugural edition of IIT Roorkee's Model United Nations conference, scheduled to take place from 17th to 19th January 2025. Your enthusiasm and commitment to being a part of this event mean a lot to us.

        After a thorough selection process, we are delighted to inform you that a portfolio has been allotted to you. Please find the details below:

        Committee: {committee}
        Portfolio: {portfolio}

        For any queries or assistance, feel free to reach out to:
        Janhavi: +91 9021774682
        Kanav: +91 9971356475
        Or write to us at irmun@iitr.ac.in

        We look forward to your meaningful contributions to MUNarchy 2025 and are excited to welcome you to this platform of dialogue and diplomacy.

        The Secretariat
        MUNarchy 2025
        IIT Roorkee Model United Nations
        Instagram: ir_mun.s

        "The Reign of Diplomacy"
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