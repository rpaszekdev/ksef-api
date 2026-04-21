"""KSeF error codes → human-readable Polish/English mapping.

Populated from CIRFMF/ksef-docs as we observe them. Week 2 day 13 extends this
map with the top 20 codes we hit during integration testing.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KsefErrorInfo:
    code: str
    pl: str
    en: str


# Seed subset — extend as we hit more
_KNOWN: dict[str, KsefErrorInfo] = {
    "21405": KsefErrorInfo(
        code="21405",
        pl="Błąd walidacji danych wejściowych. Sprawdź poprawność faktury.",
        en="Input validation error. Verify invoice payload.",
    ),
    "21418": KsefErrorInfo(
        code="21418",
        pl="Nieprawidłowy token kontynuacji.",
        en="Malformed continuation token.",
    ),
    "25001": KsefErrorInfo(
        code="25001",
        pl="Błąd zarządzania certyfikatem — nieprawidłowa struktura CSR.",
        en="Certificate management error — invalid CSR structure.",
    ),
    "30001": KsefErrorInfo(
        code="30001",
        pl="Uprawnienie już istnieje.",
        en="Entity or permission already exists.",
    ),
}


def resolve(code: str) -> KsefErrorInfo:
    return _KNOWN.get(
        code,
        KsefErrorInfo(code=code, pl="Nieznany błąd KSeF.", en="Unknown KSeF error."),
    )
