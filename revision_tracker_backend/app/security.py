# app/security.py
import bcrypt

# Bcrypt has a 72-byte limit
BCRYPT_MAX_LENGTH = 72

def _truncate_password(password: str) -> bytes:
    """
    Truncate password to bcrypt's 72-byte limit.
    Returns bytes.
    """
    password_bytes = password.encode('utf-8')
    if len(password_bytes) <= BCRYPT_MAX_LENGTH:
        return password_bytes
    
    # Truncate to exactly 72 bytes
    return password_bytes[:BCRYPT_MAX_LENGTH]

def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt directly.
    """
    password_bytes = _truncate_password(password)
    # gensalt() generates a salt, hashpw() hashes the password with the salt
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password using bcrypt directly.
    """
    try:
        password_bytes = _truncate_password(plain_password)
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False
