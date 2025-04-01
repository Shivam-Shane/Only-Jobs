import socket
import ssl
from logger import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv
import random,string
load_dotenv()
class MailSender():
    def __init__(self):
        self.SENDER_NAME_VALUE = os.getenv('SENDER_NAME')
        self.SENDER_EMAIL = os.getenv('SMTP_USERNAME')
        self.server_connection = None
        self.connect_to_smtp_server()

    def connect_to_smtp_server(self):
        try:
            logging.debug(f"Connecting to SMTP server {os.getenv('SMTP_SERVER')}")
            self.server_connection = smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT"))
            self.server_connection.starttls()
            self.server_connection.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
            logging.info("Successfully authenticated to SMTP server")
        except (socket.gaierror, socket.timeout) as net_err:
            logging.error(f"Network issue while connecting to SMTP server: {str(net_err)}")
            raise RuntimeError("Network issue while connecting to SMTP server: " + str(net_err))
        except ssl.SSLError as ssl_err:
            logging.error(f"SSL error while connecting to SMTP server: {str(ssl_err)}")
            raise RuntimeError("SSL error while connecting to SMTP server: " + str(ssl_err))
        except smtplib.SMTPException as smtp_err:
            logging.error(f"SMTP error: {str(smtp_err)}")
            raise RuntimeError("SMTP error: " + str(smtp_err))

    def forget_password_sender(self, useremail, username, password):
        """
        Sends a password reset email.
        Args:
            useremail(str): to whome to send a reset email
            username(str): Username of the receiver
            password(object): New password to be sent
        Returns:
            bool: None
        """

        body = f"""
        <html>
        <body>
            <p>Dear {username},</p>
            <p>We have received a request to reset the password for your account.</p>
            <p>Your password has been successfully reset. Please use the new password below to log in:</p>
            <p><strong>New Password: {password}</strong></p>
            <p>If you did not request a password reset, please contact us immediately.</p>
            <p>Best regards,<br>The OnlyJobs Team</p>
        </body>
        </html>
        """
        subject = "Password Reset Request"

        try:
            # Prepare the email message
            logging.debug("Preparing email message...")
            msg = MIMEMultipart()
            
            msg['From'] = f'{self.SENDER_NAME_VALUE} <{self.SENDER_EMAIL}>'
            msg['To'] = useremail
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))  # Use HTML content

            # Send the email
            self.server_connection.sendmail(os.getenv("SMTP_USERNAME"), useremail, msg.as_string())
            logging.info(f"Email sent to {useremail}")

        except smtplib.SMTPException as e:
            logging.error(f"Failed to send email: {str(e)}")
            # Reconnect and retry
            logging.info("Reconnecting to SMTP server...")
            self.connect_to_smtp_server()
            self.server_connection.sendmail(os.getenv("SMTP_USERNAME"), useremail, msg.as_string())
            logging.info(f"Email re-sent to {useremail}")

    def signup_otp_sending(self, useremail)->int:
        """
        Sends an OTP for signup.

        Args:
            useremail: To whome to send the OTP to.

        Returns:
            OTP: For cross verification of otp internally.

        """
        otp=''.join(random.choices(string.digits, k=6))
        body = f"""
        <html>
            <body>
                <p>Dear {useremail},</p>
                <p>We have received a request to sign up for your account.</p>
                <p>Your One-Time Password (OTP) is:</p>
                <p><strong>OTP: {otp}</strong></p>
                <p>Please use this OTP to complete your signup process. If you did not request a signup, You can ignore this request or contact us for more details</p>
                <p>Best regards,<br>The OnlyJobs Team</p>
            </body>
        </html>

        """
        subject = "OTP for Signup to OnlyJobs"

        try:
            # Prepare the email message
            logging.debug("Preparing email message...")
            msg = MIMEMultipart()
            
            msg['From'] = f'{self.SENDER_NAME_VALUE} <{self.SENDER_EMAIL}>'
            msg['To'] = useremail
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))  # Use HTML content

            # Send the email
            self.server_connection.sendmail(os.getenv("SMTP_USERNAME"), useremail, msg.as_string())
            logging.info(f"Email sent to {useremail}")
            return otp

        except smtplib.SMTPException as e:
            logging.error(f"Failed to send email: {str(e)}")
            # Reconnect and retry
            logging.info("Reconnecting to SMTP server...")
            self.connect_to_smtp_server()