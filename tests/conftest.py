"""Shared pytest fixtures."""

import os

# Ensure test-friendly defaults before any app import.
os.environ.setdefault("ENV", "test")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault(
    "FERNET_KEY", "5beM-gBPc_-MUCM4PTF8EvBdb-YkT0v4BSkjccom4Y8="  # 32B url-safe b64 test key
)
os.environ.setdefault("JWT_SECRET", "0" * 64)
