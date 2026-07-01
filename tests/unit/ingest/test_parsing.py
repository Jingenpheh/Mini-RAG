"""Pin the five quality_check() heuristics from mini_rag.ingest.parsing.

The heuristics gate documents before they reach chunking. Test inputs are
synthetic and small; the real text-shape signals come from langdetect, which
is mocked so the suite stays deterministic.
"""


from mini_rag.ingest.parsing import quality_check


# Reusable "looks like a real paper" body. Long enough to clear the
# MIN_CHARS gate, high alnum ratio, and contains structure markers.
GOOD_BODY = (
    "Abstract. This paper introduces a method for measuring the "
    "performance of retrieval systems on academic corpora. "
    "Introduction. We motivate the problem and survey prior work. "
    "Conclusion. The results validate the approach. References."
) * 3


def test_passes_clean_input():
    failures = quality_check(GOOD_BODY, paper_meta=None)
    assert failures == []


def test_too_short_triggers_and_short_circuits(monkeypatch):
    failures = quality_check("hi", paper_meta=None)
    assert any(f.startswith("too_short") for f in failures)
    # too_short returns immediately; no other failures should be reported
    assert len(failures) == 1


def test_low_alnum_ratio_triggers_on_garbled_text():
    garbled = ("##@@$$%%^^&&**!!" * 30) + "abstract introduction conclusion references"
    failures = quality_check(garbled, paper_meta=None)
    assert any(f.startswith("low_alnum_ratio") for f in failures)


def test_unexpected_language_triggers(monkeypatch):
    # Force langdetect to report a non-English language
    import langdetect
    monkeypatch.setattr(langdetect, "detect", lambda _text: "fr")
    failures = quality_check(GOOD_BODY, paper_meta=None)
    assert any(f.startswith("unexpected_language") for f in failures)


def test_language_detection_failure_is_reported(monkeypatch):
    import langdetect

    def boom(_text):
        raise RuntimeError("detector unavailable")

    monkeypatch.setattr(langdetect, "detect", boom)
    failures = quality_check(GOOD_BODY, paper_meta=None)
    assert "language_detection_failed" in failures


def test_no_paper_structure_markers_triggers(monkeypatch):
    # Avoid the structure-marker words entirely
    body = ("The cat sat on the mat. " * 80)
    # Stub langdetect so the language check stays clean
    import langdetect
    monkeypatch.setattr(langdetect, "detect", lambda _text: "en")
    failures = quality_check(body, paper_meta=None)
    assert "no_paper_structure_markers" in failures


def test_abstract_overlap_low_triggers_when_vocab_misses(monkeypatch):
    import langdetect
    monkeypatch.setattr(langdetect, "detect", lambda _text: "en")
    # GOOD_BODY contains "method, retrieval, academic" etc.
    # Pick an abstract whose vocabulary doesn't overlap GOOD_BODY at all.
    meta = {"abstract": "quantum chromodynamics lattice gauge tensor network simulation"}
    failures = quality_check(GOOD_BODY, paper_meta=meta)
    assert any(f.startswith("abstract_overlap_low") for f in failures)


def test_abstract_overlap_check_skipped_without_abstract(monkeypatch):
    import langdetect
    monkeypatch.setattr(langdetect, "detect", lambda _text: "en")
    # Meta present but no abstract key -> the overlap check should not run.
    failures = quality_check(GOOD_BODY, paper_meta={"title": "Whatever"})
    assert not any(f.startswith("abstract_overlap_low") for f in failures)
