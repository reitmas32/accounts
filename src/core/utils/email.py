import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from core.settings import settings,log
from enum import Enum


class SendEmailAbstract():
    def __init__(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)

    def send_email(self,email_subject:str,subject_text:str,message_text:str):
        pass
    
class GmailSendEmail(SendEmailAbstract):
    def send_email(self,email_subject,subject_text,message_text):
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(
                user = self.EMAIL_SENDER,
                password = self.EMAIL_SENDER_PASSWORD
            )
            subject = Header(subject_text, 'utf-8')
            msg = MIMEMultipart()
            msg['From'] = self.EMAIL_SENDER
            msg['To'] = email_subject
            msg['Subject'] = subject
            msg.attach(MIMEText(message_text, 'html', 'utf-8'))
            try:
                log.info("enviando mensaje")
                server.sendmail(self.EMAIL_SENDER, email_subject, msg.as_string())
            except Exception as e:
                log.error(f"******* Error al mandar mensaje, error: {e}")
            log.info("mensaje enviado....")  
            server.close()
        except Exception as e:
            print(f'Error: {e}')


class ZohoSendEmail(SendEmailAbstract):
    def send_email(self,email_sender,email_subject,subject_text,message_text):
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(
                user = self.EMAIL_SENDER,
                password = self.EMAIL_SENDER_PASSWORD
            )
            subject = Header(subject_text, 'utf-8')
            msg = MIMEMultipart()
            msg['From'] = self.EMAIL_SENDER
            msg['To'] = email_subject
            msg['Subject'] = subject
            msg.attach(MIMEText(message_text, 'html', 'utf-8'))
            try:
                log.info("enviando mensaje")
                server.sendmail(self.EMAIL_SENDER, email_subject, msg.as_string())
            except Exception as e:
                log.error(f"******* Error al mandar mensaje, error: {e}")
            log.info("mensaje enviado....")  
            server.close()
        except Exception as e:
            print(f'Error: {e}')



class SendEmailManager(Enum):
    GMAIL_SENDER = GmailSendEmail
    ZOHO_SENDER = ZohoSendEmail


def get_current_manager_email_to_app_standard():
    return SendEmailManager.GMAIL_SENDER.value(
        EMAIL_SENDER = settings.EMAIL_SENDER,
        EMAIL_SENDER_PASSWORD = settings.EMAIL_SENDER_PASSWORD
    )
