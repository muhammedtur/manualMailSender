import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email.utils import formataddr
from email import encoders

def sendEmail(receiver_email, subject, message):
    # Create a plain text message
    msg = MIMEText(message, 'plain', 'utf-8')

    # Set the sender and receiver of the email
    msg['From'] = formataddr((os.getenv('EMAIL_FROM_NAME'), os.getenv('EMAIL_USER')))
    msg['To'] = receiver_email

    # Set the subject of the email
    msg['Subject'] = Header(subject, 'utf-8')

    # Create a SMTP session
    with smtplib.SMTP_SSL(os.getenv('EMAIL_SERVER'), os.getenv('EMAIL_PORT')) as server:
        # Login to the email account
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))

        # Send the email
        server.sendmail(os.getenv('EMAIL_USER'), receiver_email, msg.as_string())
        print("Email sent successfully.")

def sendEmailWithAttachment(receiver_email, subject, message, fileName, attachment_path):
    try:
        # Create a multipart message
        msg = MIMEMultipart()

        # Add sender, receiver, and subject to the message
        msg['From'] = formataddr((os.getenv('EMAIL_FROM_NAME'), os.getenv('EMAIL_USER')))
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Add message body to the message
        msg.attach(MIMEText(message, 'html', 'utf-8'))

        # Open the file in bynary
        with open(attachment_path, 'rb') as attachment:
            # Add file as html
            part = MIMEMultipart('mixed')
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add attachment to the message
        part.add_header('Content-Disposition', f"attachment; filename= {fileName}")
        msg.attach(part)

        # Create a SMTP session
        with smtplib.SMTP_SSL(os.getenv('EMAIL_SERVER'), os.getenv('EMAIL_PORT')) as server:

            # Login to the email account
            server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))

            # Send the email
            server.sendmail(os.getenv('EMAIL_USER'), receiver_email, msg.as_string())

            print("Email sent successfully ", receiver_email)
            return True

    except Exception as e:
        print("An error occurred while sending the email:", str(e))
        return False