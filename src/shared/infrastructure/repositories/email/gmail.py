import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.utils.logger import logger
from shared.app.repositories.email.send import SendEmailRepository


class GmailSendEmail(SendEmailRepository):
    """
    Class for sending emails via Gmail.

    This class extends the SendEmailAbstract class and implements the functionality to send emails using a Gmail account.

    Attributes:
        EMAIL_SENDER (str): Email address of the sender.
        EMAIL_SENDER_PASSWORD (str): Password of the sender's email account.
    """

    def send_email(self, email_subject, subject_text, message_text):
        """
        Send an email using Gmail SMTP.

        This method sends an email with the provided subject and message texts using Gmail SMTP.

        Args:
            email_subject (str): Subject of the email.
            subject_text (str): Text content for the subject of the email.
            message_text (str): Main message content of the email.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.ehlo()
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
            except Exception as e:  # noqa: BLE001
                logger.error(f"Error sending message, error: {e}")
                return False
            logger.info("Message sent successfully")
            server.close()
            return True  # noqa: TRY300
        except Exception as e:  # noqa: BLE001
            logger.error(f"Error: {e}")
            return False
