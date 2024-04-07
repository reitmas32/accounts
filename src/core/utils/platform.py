import hashlib


class PlatformIDHasher:
    """
    A class dedicated to hashing platform IDs for secure and efficient storage and lookup.
    """

    @staticmethod
    def hash_hashed_platform_id(hashed_platform_id: str) -> str:
        """
        Hashes the hashed_platform_id  using SHA-256 and returns the hash as a hexadecimal string.

        Args:
            hashed_platform_id  (str): The platform ID to be hashed.

        Returns:
            str: The hexadecimal string of the hashed platform ID.
        """
        # Encode the platform ID to bytes.
        encoded_id = hashed_platform_id.encode()
        # Create a SHA-256 hash object.
        hash_object = hashlib.sha256(encoded_id)
        # Return the hexadecimal digest of the platform ID.
        return hash_object.hexdigest()
