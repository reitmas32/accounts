from shared.app.enums.email_clients import EmailClientsEnum
from shared.app.errors.unimplemented import UnimplementedError
from shared.infrastructure.repositories.email.gmail import GmailSendEmail
from shared.infrastructure.repositories.email.zoho import ZohoSendEmail


class EmailManager:

    def __init__(self, client: str):
        if client == EmailClientsEnum.GMAIL:
            self.client = GmailSendEmail
        elif client == EmailClientsEnum.ZOHO:
            self.client = ZohoSendEmail
        else:
            self.client = None
            raise UnimplementedError(message="EmailClient")



def hide_email(email):
    # Split the email into username and domain
    username, domain = email.split("@")

    # Hide part of the username
    hidden = username[0] + "*" * (len(username) - 2) + username[-1]

    # Reconstruct the hidden email
    return hidden + "@" + domain
