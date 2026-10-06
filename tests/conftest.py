import pytest


@pytest.fixture(autouse=True)
def _isolated_cache(tmp_path, monkeypatch):
    """Tests never touch the real spend ledger or LLM cache."""
    monkeypatch.setenv("GF_CACHE_DIR", str(tmp_path / "gf_cache"))
    monkeypatch.setenv("GF_SPEND_CAP_USD", "1.0")
