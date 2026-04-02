# utils/email.py

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

def send_login_email(to_email: str, user_id: str, nickname: str) -> bool:
    """
    Send login information to the user's email.
    Returns True if email was sent successfully.
    """
    try:
        # Get credentials from .env
        smtp_email = os.getenv("SMTP_EMAIL")
        smtp_password = os.getenv("SMTP_PASSWORD")
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))

        if not smtp_email or not smtp_password:
            print("ERROR: SMTP_EMAIL or SMTP_PASSWORD not set in .env file")
            return False

        # Create email message
        msg = MIMEMultipart()
        msg['From'] = smtp_email
        msg['To'] = to_email
        msg['Subject'] = "Your Niv Louie Login Information"

        body = f"""Hello {nickname},

Here is your Niv Louie login information:

User ID: {user_id}
Nickname: {nickname}

IMPORTANT:
• Save this information in a safe place.
• You will need this User ID to log in from any device.
• If there is no activity for 6 months, the account will be automatically deleted.

Thank you for using Niv Louie!

Best regards,
Niv Louie Team
"""

        msg.attach(MIMEText(body, 'plain'))

        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
        server.quit()

        print(f"LOG: Login email sent successfully to {to_email}")
        return True

    except Exception as e:
        print(f"ERROR: Failed to send email: {e}")
        return False