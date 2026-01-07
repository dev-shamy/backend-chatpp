import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Pre-hash the password with SHA256 to fix length limitation
    sha256_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # Now bcrypt the fixed-length hex string
    return pwd_context.hash(sha256_hash)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha256_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return pwd_context.verify(sha256_hash, hashed_password)
