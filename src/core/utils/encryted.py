import cryptocode

from core.utils.exceptions import EncryptedException


class EncryptedController:
    def __init__(self, key: str | None = None):
        if key is None or key == "":
            raise EncryptedException("The encryption key must not be null")
        self.key = key

    def encrypt(self, data: str) -> str:
        return cryptocode.encrypt(data, self.key)

    def decrypt(self, encrypted_data: str) -> str:
        return cryptocode.decrypt(encrypted_data, self.key)
