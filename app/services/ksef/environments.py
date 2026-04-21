"""KSeF environment URL resolver (test / demo / prod)."""

from typing import Literal

KsefEnv = Literal["test", "demo", "prod"]

BASE_URLS: dict[KsefEnv, str] = {
    "test": "https://api-test.ksef.mf.gov.pl/v2",
    "demo": "https://api-demo.ksef.mf.gov.pl/v2",
    "prod": "https://api.ksef.mf.gov.pl/v2",
}


def base_url_for(env: KsefEnv) -> str:
    try:
        return BASE_URLS[env]
    except KeyError as e:
        raise ValueError(f"Unknown KSeF env: {env}") from e
