import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum

from core.settings import log, settings


class SendEmailAbstract:
    """
    Abstract class for sending emails.

    This class serves as a base for implementing email sending functionality. It provides a placeholder method for sending emails.

    Args:
        **kwargs: Additional keyword arguments.

    Attributes:
        **kwargs: Additional attributes specified during initialization.
    """

    def __init__(self, **kwargs):
        """
        Initialize the SendEmailAbstract.

        Args:
            **kwargs: Additional keyword arguments.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def send_email(self, email_subject: str, subject_text: str, message_text: str):
        """
        Send an email.

        This method sends an email with the provided subject and message texts.

        Args:
            email_subject (str): Subject of the email.
            subject_text (str): Text content for the subject of the email.
            message_text (str): Main message content of the email.
        """


class GmailSendEmail(SendEmailAbstract):
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
                log.info("Sending message")
                server.sendmail(self.EMAIL_SENDER, email_subject, msg.as_string())
            except Exception as e:  # noqa: BLE001
                log.error(f"Error sending message, error: {e}")
                return False
            log.info("Message sent successfully")
            server.close()
            return True  # noqa: TRY300
        except Exception as e:  # noqa: BLE001
            log.error(f"Error: {e}")
            return False


class ZohoSendEmail(SendEmailAbstract):
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
                log.info("Sending message")
                server.sendmail(self.EMAIL_SENDER, email_subject, msg.as_string())
                server.quit()
            except Exception as e:  # noqa: BLE001
                log.error(f"Error sending message, error: {e}")
            log.info("Message sent successfully")
            server.close()
        except Exception as e:  # noqa: BLE001
            log.error(f"Error: {e}")


class SendEmailManager(Enum):
    """
    Enum class for managing different email sender implementations.

    This enum class provides options for selecting different email sender implementations, such as Gmail or Zoho.

    Enum Values:
        GMAIL_SENDER: Gmail email sender implementation.
        ZOHO_SENDER: Zoho email sender implementation.
    """

    GMAIL_SENDER = GmailSendEmail
    ZOHO_SENDER = ZohoSendEmail


def get_current_manager_email_to_app_standard():
    """
    Get the current email manager configured for the application.

    This function returns an instance of the email sender manager configured to use the Gmail email sender implementation.

    Returns:
        SendEmailAbstract: An instance of the email sender manager.
    """
    return SendEmailManager.ZOHO_SENDER.value(
        EMAIL_SENDER=settings.EMAIL_SENDER, EMAIL_SENDER_PASSWORD=settings.EMAIL_SENDER_PASSWORD
    )


def hide_email(email):
    # Split the email into username and domain
    username, domain = email.split("@")

    # Hide part of the username
    hidden = username[0] + "*" * (len(username) - 2) + username[-1]

    # Reconstruct the hidden email
    return hidden + "@" + domain
