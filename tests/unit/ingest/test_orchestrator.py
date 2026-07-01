"""Pin orchestrator versioning helpers.

config_hash determinism is the dedup contract: same inputs -> same key.
pipeline_commit must fall back gracefully when git is unavailable so
ingestion runs work in environments without git on PATH.
"""

import subprocess


from mini_rag.ingest import orchestrator


def test_compute_config_hash_is_deterministic():
    first = orchestrator.compute_config_hash()
    second = orchestrator.compute_config_hash()
    assert first == second


def test_compute_config_hash_is_eight_hex_chars():
    h = orchestrator.compute_config_hash()
    assert len(h) == 8
    int(h, 16)  # would raise ValueError if not hex


def test_compute_config_hash_changes_when_config_changes(monkeypatch):
    original = orchestrator.compute_config_hash()

    # Bump the version constant. compute_config_hash imports lazily from
    # config inside its body, so monkeypatching config.CHUNKER_VERSION
    # changes the hash on the next call.
    import config
    monkeypatch.setattr(config, "CHUNKER_VERSION", config.CHUNKER_VERSION + 100)
    changed = orchestrator.compute_config_hash()
    assert changed != original


def test_compute_pipeline_commit_returns_unknown_when_git_missing(monkeypatch):
    def boom(*args, **kwargs):
        raise FileNotFoundError("git not on PATH")
    monkeypatch.setattr(subprocess, "run", boom)
    assert orchestrator.compute_pipeline_commit() == "unknown"


def test_compute_pipeline_commit_returns_unknown_on_nonzero_exit(monkeypatch):
    class _Result:
        returncode = 128
        stdout = ""
        stderr = "fatal: not a git repository"

    monkeypatch.setattr(subprocess, "run", lambda *a, **k: _Result())
    assert orchestrator.compute_pipeline_commit() == "unknown"


def test_compute_pipeline_commit_returns_stripped_stdout(monkeypatch):
    class _Result:
        returncode = 0
        stdout = "abc1234\n"
        stderr = ""

    monkeypatch.setattr(subprocess, "run", lambda *a, **k: _Result())
    assert orchestrator.compute_pipeline_commit() == "abc1234"
