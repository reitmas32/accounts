import random
import string


def generate_code(length):
    """
    Generate a verification code.

    Args:
        length (int): Length of the verification code.

    Returns:
        str: Generated verification code.
    """
    return "".join(random.choices(string.digits, k=length))  # noqa: S311
