from passlib.context import CryptContext

from core.settings import settings


class PasswordHandler:
    # Creates a Passlib context with the selected algorithm
    pwd_context = CryptContext(schemes=[settings.HASHING_ALGORITHM.value], deprecated="auto")

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Encrypts the provided password using the algorithm specified in the global configuration.

        :param password: The plaintext password to be hashed.
        :return: A string representing the hashed password.
        """
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Verifies whether a plaintext password matches its hashed version.

        :param plain_password: The plaintext password to verify.
        :param hashed_password: The stored hashed password to compare against.
        :return: True if the passwords match, False otherwise.
        """
        return cls.pwd_context.verify(plain_password, hashed_password)
