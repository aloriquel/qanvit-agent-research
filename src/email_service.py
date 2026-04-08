import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, RECIPIENT_EMAIL

class EmailService:
    def send_email(self, subject, html_content):
        """Send the report via email."""
        msg = MIMEMultipart('related')
        msg['From'] = SMTP_USERNAME
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject

        template = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #F8FAFC; color: #1F2937; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; border-top: 5px solid #0F172A; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
                h1, h2, h3 {{ color: #0F172A; }}
                a {{ color: #0284C7; text-decoration: none; }}
                .cta-button {{ display: inline-block; background-color: #E0F2FE; color: #0F172A; padding: 12px 24px; text-decoration: none; font-weight: bold; border-radius: 4px; margin-top: 20px; }}
                .signature {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #eaeaea; }}
            </style>
        </head>
        <body>
            <div class="container">
                {html_content}
                <div style="text-align: center; margin-top: 40px;">
                    <a href="https://www.qanvit.com" class="cta-button">Visitar qanvit.com</a>
                </div>
                <div class="signature">
                    <p><b>Qanvit CI Agent</b></p>
                </div>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(template, 'html'))

        try:
            print(f"Connecting to {SMTP_SERVER}...")
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, RECIPIENT_EMAIL, msg.as_string())
            server.quit()
            print("Email sent successfully!")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
