import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.utils.logger import logger
from shared.app.repositories.email.send import SendEmailRepository


class ZohoSendEmail(SendEmailRepository):
    """
    Class for sending emails via Zoho.

    This class extends the SendEmailAbstract class and implements the functionality to send emails using Zoho SMTP.

    Attributes:
        EMAIL_SENDER (str): Email address of the sender.
        EMAIL_SENDER_PASSWORD (str): Password of the sender's email account.
    """

    def send_email(self, email_subject, subject_text, message_text):
        """
        Send an email using Zoho SMTP.

        This method sends an email with the provided subject and message texts using Zoho SMTP.

        Args:
            email_subject (str): Subject of the email.
            subject_text (str): Text content for the subject of the email.
            message_text (str): Main message content of the email.
        """
        try:
            server = smtplib.SMTP_SSL("smtp.zoho.com", 465)

            # Perform operations via server
            server.login(user=self.EMAIL_SENDER, password=self.EMAIL_SENDER_PASSWORD)
            subject = Header(subject_text, "utf-8")
            msg = MIMEMultipart()
            msg["From"] = self.EMAIL_SENDER
            msg["To"] = email_subject
            msg["Subject"] = subject
            msg.attach(MIMEText(message_text, "html", "utf-8"))
            try:
                logger.info("Sending message")
                server.sendmail(self.EMAIL_SENDER, email_subject, msg.as_string())
                server.quit()
            except Exception as e:  # noqa: BLE001
                logger.error(f"Error sending message, error: {e}")
            logger.info("Message sent successfully")
            server.close()
        except Exception as e:  # noqa: BLE001
            logger.error(f"Error: {e}")
