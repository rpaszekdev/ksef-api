"""Verify API key generation + hashing is deterministic and safe."""

import re

from app.core.security import generate_api_key, hash_api_key


def test_generate_api_key_shape() -> None:
    raw, prefix, digest = generate_api_key()
    assert raw.startswith("ksef_")
    assert len(raw) >= 20
    assert prefix == raw[:12]
    assert re.fullmatch(r"[0-9a-f]{64}", digest)


def test_hash_api_key_deterministic() -> None:
    raw, _, digest = generate_api_key()
    assert hash_api_key(raw) == digest


def test_generate_api_key_unique() -> None:
    seen = {generate_api_key()[0] for _ in range(100)}
    assert len(seen) == 100
