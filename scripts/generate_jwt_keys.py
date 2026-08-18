from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


KEYS_DIR = Path("../secrets")
KEYS_DIR.mkdir(exist_ok=True)


private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3072,
)

private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

public_pem = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

(KEYS_DIR / "jwt_private.pem").write_bytes(private_pem)
(KEYS_DIR / "jwt_public.pem").write_bytes(public_pem)

print("JWT RSA key pair generated successfully.")
print(f"Private key: {KEYS_DIR / 'jwt_private.pem'}")
print(f"Public key:  {KEYS_DIR / 'jwt_public.pem'}")