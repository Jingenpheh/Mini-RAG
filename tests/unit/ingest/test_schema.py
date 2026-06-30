"""Pin the Chunk.to_metadata() contract that mini_rag.ingest.storage relies on."""

from mini_rag.ingest.schema import Chunk


def _chunk(**overrides) -> Chunk:
    defaults = dict(
        chunk_id="2606.00001::00000",
        text="Some chunk text.",
        chunk_index=0,
        arxiv_id="2606.00001",
        title="A Paper Title",
        authors=["Alice", "Bob"],
        published_at="2026-06-01T00:00:00",
        categories=["cs.AI", "cs.LG"],
        primary_category="cs.AI",
        section_heading="Introduction",
        doc_item_labels=["text"],
        char_count=16,
        pipeline_commit="abc123",
        config_hash="def45678",
        ingested_at="2026-06-30T12:00:00",
    )
    defaults.update(overrides)
    return Chunk(**defaults)


def test_to_metadata_excludes_text_and_chunk_id():
    md = _chunk().to_metadata()
    assert "text" not in md
    assert "chunk_id" not in md


def test_to_metadata_joins_list_fields_with_semicolon_space():
    md = _chunk(
        authors=["Alice", "Bob", "Carol"],
        categories=["cs.AI", "cs.LG"],
        doc_item_labels=["text", "list_item"],
    ).to_metadata()
    assert md["authors"] == "Alice; Bob; Carol"
    assert md["categories"] == "cs.AI; cs.LG"
    assert md["doc_item_labels"] == "text; list_item"


def test_to_metadata_handles_empty_lists():
    md = _chunk(authors=[], categories=[], doc_item_labels=[]).to_metadata()
    assert md["authors"] == ""
    assert md["categories"] == ""
    assert md["doc_item_labels"] == ""


def test_to_metadata_preserves_scalar_fields():
    md = _chunk(
        arxiv_id="2606.00042",
        title="Title Here",
        chunk_index=7,
        char_count=512,
        section_heading="Methods",
        config_hash="abcd1234",
        pipeline_commit="0badcafe",
        published_at="2026-06-15T00:00:00",
        primary_category="cs.LG",
        access_level="public",
        ingested_at="2026-06-30T12:00:00",
    ).to_metadata()
    assert md["arxiv_id"] == "2606.00042"
    assert md["title"] == "Title Here"
    assert md["chunk_index"] == 7
    assert md["char_count"] == 512
    assert md["section_heading"] == "Methods"
    assert md["config_hash"] == "abcd1234"
    assert md["pipeline_commit"] == "0badcafe"
    assert md["primary_category"] == "cs.LG"
    assert md["access_level"] == "public"


def test_to_metadata_values_are_chroma_safe_primitives():
    md = _chunk().to_metadata()
    for key, value in md.items():
        assert isinstance(value, (str, int, float, bool)), \
            f"non-primitive metadata value for {key}: {type(value).__name__}"
