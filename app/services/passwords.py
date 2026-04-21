"""Password hashing wrapper around bcrypt.

Uses bcrypt directly (not passlib) to avoid the passlib/bcrypt 4.x
detect-wrap-bug check that rejects passwords > 72 bytes during backend init.
"""

import bcrypt

_MAX_BYTES = 72  # bcrypt's hard input limit


def _truncate(password: str) -> bytes:
    raw = password.encode("utf-8")
    return raw[:_MAX_BYTES]


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(_truncate(password), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(_truncate(password), password_hash.encode("utf-8"))
    except ValueError:
        return False
