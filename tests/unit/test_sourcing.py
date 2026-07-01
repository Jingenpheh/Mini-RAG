"""Pin sourcing helpers used by scripts/sourcing/fetch_papers.py.

The arXiv API I/O is not exercised here; arxiv.Client is the boundary.
What's tested is the pure-Python logic that sits in front of the API:
canonical ID derivation, query string composition, and manifest dedup.
"""




def test_canonical_arxiv_id_strips_version_suffix():
    from scripts.sourcing.fetch_papers import canonical_arxiv_id
    assert canonical_arxiv_id("http://arxiv.org/abs/2606.20457v2") == "2606.20457"


def test_canonical_arxiv_id_handles_no_version():
    from scripts.sourcing.fetch_papers import canonical_arxiv_id
    assert canonical_arxiv_id("http://arxiv.org/abs/2606.20457") == "2606.20457"


def test_canonical_arxiv_id_handles_https_scheme():
    from scripts.sourcing.fetch_papers import canonical_arxiv_id
    assert canonical_arxiv_id("https://arxiv.org/abs/2606.20457v1") == "2606.20457"


def test_canonical_arxiv_id_handles_bare_id():
    from scripts.sourcing.fetch_papers import canonical_arxiv_id
    assert canonical_arxiv_id("2606.20457") == "2606.20457"


def test_build_query_includes_all_categories(monkeypatch):
    import scripts.sourcing.fetch_papers as fp
    monkeypatch.setattr(fp, "CATEGORIES", ["cs.AI", "cs.LG"])
    monkeypatch.setattr(fp, "KEYWORDS", [])
    q = fp.build_query()
    assert "cat:cs.AI" in q
    assert "cat:cs.LG" in q
    assert " OR " in q


def test_build_query_adds_keyword_clause(monkeypatch):
    import scripts.sourcing.fetch_papers as fp
    monkeypatch.setattr(fp, "CATEGORIES", ["cs.AI"])
    monkeypatch.setattr(fp, "KEYWORDS", ["retrieval", "rerank"])
    q = fp.build_query()
    assert 'all:"retrieval"' in q
    assert 'all:"rerank"' in q
    assert " AND " in q


def test_build_query_no_keyword_clause_when_keywords_empty(monkeypatch):
    import scripts.sourcing.fetch_papers as fp
    monkeypatch.setattr(fp, "CATEGORIES", ["cs.AI"])
    monkeypatch.setattr(fp, "KEYWORDS", [])
    q = fp.build_query()
    assert "all:" not in q


def test_load_manifest_returns_empty_dict_when_missing(monkeypatch, tmp_path):
    import scripts.sourcing.fetch_papers as fp
    monkeypatch.setattr(fp, "MANIFEST_PATH", tmp_path / "nope.json")
    assert fp.load_manifest() == {}


def test_save_then_load_manifest_roundtrip(monkeypatch, tmp_path):
    import scripts.sourcing.fetch_papers as fp
    monkeypatch.setattr(fp, "MANIFEST_PATH", tmp_path / "manifest.json")
    payload = {"2606.00001": {"title": "Sample", "filename": "2606.00001.pdf"}}
    fp.save_manifest(payload)
    assert fp.load_manifest() == payload
