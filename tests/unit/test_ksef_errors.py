from app.services.ksef.errors import resolve


def test_known_error() -> None:
    info = resolve("21405")
    assert info.code == "21405"
    assert "walidacji" in info.pl.lower()
    assert "validation" in info.en.lower()


def test_unknown_error() -> None:
    info = resolve("99999")
    assert info.code == "99999"
    assert "unknown" in info.en.lower()
