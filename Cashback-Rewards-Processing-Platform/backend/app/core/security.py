# app/core/security.py

import hashlib
import hmac
import re

import bcrypt
from cryptography.fernet import Fernet, InvalidToken

from app.core.config import settings

_fernet: Fernet | None = None


def _get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        raw = settings.FIELD_ENCRYPTION_KEY.strip().strip("'").strip('"')
        try:
            _fernet = Fernet(raw.encode("utf-8"))
        except ValueError as exc:
            raise ValueError(
                "FIELD_ENCRYPTION_KEY is invalid. "
                "Generate one with: "
                'uv run python -c "from cryptography.fernet import Fernet; '
                'print(Fernet.generate_key().decode())" '
                "then set FIELD_ENCRYPTION_KEY=<generated-value> in .env "
                "(no quotes, no spaces)."
            ) from exc
    return _fernet


def hash_password(password: str) -> str:
    """
    Hash a plaintext password for storage.
    """

    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plaintext password against a stored hash.
    """

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def normalize_mobile(mobile_number: str) -> str:
    """
    Normalize a mobile number for hashing and storage consistency.
    Keeps digits and a leading '+'; strips other characters.
    """

    cleaned = mobile_number.strip()
    has_plus = cleaned.startswith("+")
    digits = re.sub(r"\D", "", cleaned)
    if has_plus:
        return f"+{digits}"
    return digits


def hash_mobile(mobile_number: str) -> str:
    """
    Deterministic HMAC hash for exact-match filtering.
    Not reversible — used only for lookup / uniqueness.
    """

    normalized = normalize_mobile(mobile_number)
    secret = (
        settings.FIELD_ENCRYPTION_KEY.strip().strip("'").strip('"')
    )
    digest = hmac.new(
        secret.encode("utf-8"),
        normalized.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return digest


def encrypt_mobile(mobile_number: str) -> str:
    """
    Encrypt a mobile number for at-rest storage.
    """

    normalized = normalize_mobile(mobile_number)
    token = _get_fernet().encrypt(normalized.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_mobile(mobile_encrypted: str) -> str:
    """
    Decrypt a stored mobile number for API responses.
    """

    try:
        plaintext = _get_fernet().decrypt(
            mobile_encrypted.encode("utf-8")
        )
    except InvalidToken as exc:
        raise ValueError(
            "Unable to decrypt mobile number."
        ) from exc

    return plaintext.decode("utf-8")
