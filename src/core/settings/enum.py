from enum import Enum


class HashingAlgorithmsEnum(Enum):
    """
    Manages password hashing and verification using secure algorithms. Each algorithm is recommended
    for different use cases, considering security, performance, and compatibility:

    - BCRYPT: Recommended for general applications where security is important but performance is not critical.
      Provides a good balance between security and speed. Suitable for most web applications.

    - ARGON2: Most recommended for situations where security is critical. Winner of the Password Hashing Competition,
      designed to resist brute-force attacks on both specialized and general hardware. Features adjustable parameters
      for memory, CPU, and parallelism, allowing detailed configuration based on the deployment environment.

    - SCRYPT: Designed to be memory-intensive, making it more resistant against attacks using specialized hardware.
      Recommended for systems that can afford intensive resource usage to increase security. A good choice if brute-force
      attacks are a significant concern and sufficient memory is available.

    - PBKDF2_SHA256: A well-established standard using SHA-256. While not as resistant as Argon2 or scrypt against
      specialized hardware, it remains a solid choice due to its broad compatibility. Recommended for systems needing
      to interoperate with other platforms or technologies that already implement PBKDF2.

    The choice of algorithm should be based on an assessment of the specific application environment, including security
    requirements, system resource availability, and the need for compatibility with other technologies or frameworks.
    """

    BCRYPT = "bcrypt"
    ARGON2 = "argon2"
    SCRYPT = "scrypt"
    PBKDF2_SHA256 = "pbkdf2_sha256"


class JWTAlgorithmsEnum(Enum):
    """
    Enumerates JWT algorithms and provides recommendations based on security, performance, and compatibility.

    - HS256: HMAC using SHA-256.Recommended for simple authentication systems where a shared secret is acceptable.
      Suitable for internal applications or systems where tokens are only validated by one party.

    - RS256: RSA using SHA-256.Recommended for distributed systems where tokens are issued and validated by different
      parties.Suitable for applications needing to share a public key for token validation without exposing the private key.

    - ES256: ECDSA using P-256 and SHA-256. Recommended for high-security applications due to its strong security with shorter
      key lengths compared to RSA, leading to faster processing and less bandwidth usage. Suitable for performance-sensitive applications.

    - PS256: RSA PSS using SHA-256. Provides a higher security level than RS256 by using a probabilistic signature scheme.
      Recommended for environments requiring enhanced security measures.

    The choice of algorithm should be based on the application's security requirements, the infrastructure's capability to handle
    cryptographic operations, and the need for interoperability with other services or applications.
    """

    HS256 = "HS256"
    RS256 = "RS256"
    ES256 = "ES256"
    PS256 = "PS256"
