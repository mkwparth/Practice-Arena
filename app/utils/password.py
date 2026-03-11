import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def preprocess_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password(password: str):

    password = preprocess_password(password)

    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):

    password = preprocess_password(password)

    return pwd_context.verify(password, hashed)