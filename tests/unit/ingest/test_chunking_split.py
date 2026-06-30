"""Pin _split_long_text behavior. Pure-string sentence-boundary splitting."""

from mini_rag.ingest.chunking import _split_long_text


def test_returns_input_unchanged_when_under_ceiling():
    text = "One sentence. Two sentence. Three sentence."
    pieces = _split_long_text(text, ceiling=1000)
    assert pieces == [text]


def test_splits_on_sentence_boundary_when_over_ceiling():
    # Two short sentences. With a tight ceiling, each lands in its own piece.
    text = "First sentence is short. Second sentence is also short."
    pieces = _split_long_text(text, ceiling=30)
    assert len(pieces) == 2
    assert pieces[0].startswith("First")
    assert pieces[1].startswith("Second")


def test_accumulates_sentences_under_ceiling():
    text = "Aaa. Bbb. Ccc. Ddd."
    # Ceiling generous enough to hold two sentences but not all four
    pieces = _split_long_text(text, ceiling=10)
    # Every piece must be <= ceiling
    for piece in pieces:
        assert len(piece) <= 10
    # All sentence content is preserved
    rejoined = " ".join(pieces)
    for sent in ("Aaa.", "Bbb.", "Ccc.", "Ddd."):
        assert sent in rejoined


def test_handles_empty_input():
    assert _split_long_text("", ceiling=100) == [""]


def test_oversized_single_sentence_left_as_is():
    # If a sentence exceeds the ceiling with no internal punctuation, the
    # function leaves it whole rather than cutting mid-sentence.
    long_sentence = "a" * 500
    pieces = _split_long_text(long_sentence, ceiling=100)
    assert pieces == [long_sentence]
