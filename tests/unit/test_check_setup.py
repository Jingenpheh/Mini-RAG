"""Pin individual deployment checks in mini_rag.check_setup.

The check functions are split from the monolithic check_setup() so each can
be exercised with a small mock setup. The orchestrator's printing and exit
code are not unit-tested here; that's covered by running the script in
practice.
"""

import os

import pytest


def test_check_openai_key_passes_when_env_set(monkeypatch):
    from mini_rag.check_setup import check_openai_key
    monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
    ok, _ = check_openai_key()
    assert ok is True


def test_check_openai_key_fails_when_missing(monkeypatch):
    from mini_rag.check_setup import check_openai_key
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    # Prevent .env autoload from rescuing the check
    monkeypatch.setattr(
        "mini_rag.check_setup._load_dotenv_if_available",
        lambda: None,
    )
    ok, detail = check_openai_key()
    assert ok is False
    assert "OPENAI_API_KEY" in detail or detail  # detail is non-empty


def test_check_corpus_dir_passes_for_real_dir(tmp_path):
    from mini_rag.check_setup import check_corpus_dir
    ok, _ = check_corpus_dir(str(tmp_path))
    assert ok is True


def test_check_corpus_dir_fails_for_missing_path(tmp_path):
    from mini_rag.check_setup import check_corpus_dir
    missing = tmp_path / "does_not_exist"
    ok, _ = check_corpus_dir(str(missing))
    assert ok is False


def test_check_chroma_dir_passes_when_parent_exists(tmp_path):
    from mini_rag.check_setup import check_chroma_dir
    # Path itself doesn't exist, but its parent does
    target = tmp_path / "chroma"
    ok, _ = check_chroma_dir(str(target))
    assert ok is True


def test_check_chroma_dir_fails_when_parent_missing(tmp_path):
    from mini_rag.check_setup import check_chroma_dir
    target = tmp_path / "missing_parent" / "chroma"
    ok, _ = check_chroma_dir(str(target))
    assert ok is False


def test_check_mcp_importable_passes_on_real_install():
    from mini_rag.check_setup import check_mcp_importable
    ok, _ = check_mcp_importable()
    assert ok is True  # mcp is a runtime dep


def test_check_vector_store_handles_unreachable_store(monkeypatch):
    from mini_rag.check_setup import check_vector_store

    class _Boom:
        def __getattr__(self, _):
            raise RuntimeError("not connected")

    monkeypatch.setattr("mini_rag.utils.get_vector_store", lambda: _Boom())
    ok, count, detail = check_vector_store()
    assert ok is False
    assert count == -1
    assert detail  # non-empty failure detail
