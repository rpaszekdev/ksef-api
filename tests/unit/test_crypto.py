"""Round-trip Fernet encrypt/decrypt."""

from app.services.crypto import decrypt, encrypt


def test_round_trip() -> None:
    plaintext = "ya29.access-token-example-very-secret"
    cipher = encrypt(plaintext)
    assert cipher != plaintext
    assert decrypt(cipher) == plaintext


def test_two_encryptions_differ() -> None:
    a = encrypt("same")
    b = encrypt("same")
    # Fernet includes a nonce so ciphertexts must differ even for same plaintext
    assert a != b
