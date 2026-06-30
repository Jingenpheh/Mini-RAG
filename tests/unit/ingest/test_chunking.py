"""Pin chunk_document() behavior. Uses fakes injected via conftest.py.

The fakes are duck types for Docling items; conftest's
install_docling_class_fakes fixture monkeypatches docling's module-level
class names so the chunker's isinstance() checks see the fakes as the real
types. This lets the full chunk_document() pipeline run without ever
parsing a PDF.
"""

import pytest

from mini_rag.ingest.chunking import chunk_document
from tests.conftest import (
    FakeFormulaItem,
    FakeSectionHeader,
    FakeTableItem,
    FakeTextItem,
    fake_doc,
)


RUN_META = {
    "pipeline_commit": "abc123",
    "config_hash": "def45678",
    "ingested_at": "2026-06-30T12:00:00",
}


def _chunk(doc, arxiv_id="2606.00001", paper_meta=None):
    return chunk_document(
        doc,
        arxiv_id=arxiv_id,
        paper_meta=paper_meta or {"title": "T", "authors": [], "categories": []},
        run_meta=RUN_META,
    )


# Pass-2: merge floor ##########################################################

def test_small_same_section_items_merge(install_docling_class_fakes):
    doc = fake_doc([
        FakeSectionHeader("Introduction"),
        FakeTextItem("Short one." * 3, label="text"),   # < 200 chars
        FakeTextItem("Short two." * 3, label="text"),   # < 200 chars
    ])
    chunks = _chunk(doc)
    assert len(chunks) == 1
    assert "Short one." in chunks[0].text
    assert "Short two." in chunks[0].text


def test_items_in_different_sections_do_not_merge(install_docling_class_fakes):
    doc = fake_doc([
        FakeSectionHeader("Intro"),
        FakeTextItem("Short A." * 4, label="text"),
        FakeSectionHeader("Methods"),
        FakeTextItem("Short B." * 4, label="text"),
    ])
    chunks = _chunk(doc)
    assert len(chunks) == 2
    assert chunks[0].section_heading == "Intro"
    assert chunks[1].section_heading == "Methods"


def test_items_with_different_labels_do_not_merge(install_docling_class_fakes):
    doc = fake_doc([
        FakeSectionHeader("Intro"),
        FakeTextItem("Short text." * 3, label="text"),
        FakeTextItem("Short item." * 3, label="list_item"),
    ])
    chunks = _chunk(doc)
    assert len(chunks) == 2


# Pass-3: drop floor and size ceiling ##########################################

def test_items_under_drop_floor_are_dropped(install_docling_class_fakes):
    doc = fake_doc([FakeTextItem("tiny", label="text")])  # 4 chars < 30
    assert _chunk(doc) == []


def test_oversized_item_splits_on_sentence_boundary(install_docling_class_fakes):
    # Build a chunk above the ceiling out of repeated short sentences.
    sentence = "This is a sentence. "
    body = sentence * 200  # well above 2000 chars
    doc = fake_doc([FakeTextItem(body, label="text")])
    chunks = _chunk(doc)
    assert len(chunks) > 1
    # The contextual prefix adds a fixed overhead; cap is on the body itself,
    # so allow some headroom. Each chunk's text length stays bounded.
    for c in chunks:
        # 2000 char ceiling + prefix (~50 chars at most for "Paper: T")
        assert len(c.text) <= 2100


# Pass-1: formula handling #####################################################

def test_formula_attaches_to_preceding_chunk(install_docling_class_fakes):
    doc = fake_doc([
        FakeTextItem("Leading explanation text " * 10, label="text"),
        FakeFormulaItem(text="E = mc^2"),
    ])
    chunks = _chunk(doc)
    assert len(chunks) == 1
    assert "E = mc^2" in chunks[0].text


def test_formula_falls_back_to_orig_when_text_is_empty(install_docling_class_fakes):
    doc = fake_doc([
        FakeTextItem("Leading text " * 20, label="text"),
        FakeFormulaItem(text="", orig="\\alpha = \\beta"),
    ])
    chunks = _chunk(doc)
    assert "\\alpha = \\beta" in chunks[0].text


def test_failed_formula_does_not_attach(install_docling_class_fakes):
    doc = fake_doc([
        FakeTextItem("Leading text " * 20, label="text"),
        FakeFormulaItem(text="formula-not-decoded blah"),
    ])
    chunks = _chunk(doc)
    assert "formula-not-decoded" not in chunks[0].text


# Pass-1: table handling #######################################################

def test_table_rendered_as_markdown(install_docling_class_fakes):
    md = "| col1 | col2 |\n|------|------|\n| 1 | 2 |"
    doc = fake_doc([FakeTableItem(md)])
    chunks = _chunk(doc)
    assert len(chunks) == 1
    assert "col1" in chunks[0].text
    assert "col2" in chunks[0].text
    assert chunks[0].doc_item_labels == ["table"]


# Pass-4: contextual prefix ####################################################

def test_prefix_includes_paper_title_and_section(install_docling_class_fakes):
    doc = fake_doc([
        FakeSectionHeader("Methods"),
        FakeTextItem("Body content here " * 20, label="text"),
    ])
    chunks = _chunk(doc, paper_meta={"title": "My Cool Paper"})
    assert chunks[0].text.startswith("Paper: My Cool Paper\nSection: Methods\n\n")


def test_prefix_omits_section_line_when_section_missing(install_docling_class_fakes):
    doc = fake_doc([FakeTextItem("Body content here " * 20, label="text")])
    chunks = _chunk(doc, paper_meta={"title": "My Cool Paper"})
    assert chunks[0].text.startswith("Paper: My Cool Paper\n\n")
    assert "Section:" not in chunks[0].text.split("\n\n")[0]


def test_prefix_skipped_when_title_and_section_both_missing(install_docling_class_fakes):
    doc = fake_doc([FakeTextItem("Body content here " * 20, label="text")])
    chunks = _chunk(doc, paper_meta={"title": ""})
    assert not chunks[0].text.startswith("Paper:")


# Pass-5: chunk_id format ######################################################

def test_chunk_id_format(install_docling_class_fakes):
    doc = fake_doc([
        FakeTextItem("First chunk content " * 20, label="text"),
        FakeSectionHeader("Methods"),
        FakeTextItem("Second chunk content " * 20, label="text"),
    ])
    chunks = _chunk(doc, arxiv_id="2606.00042")
    assert chunks[0].chunk_id == "2606.00042::00000"
    assert chunks[1].chunk_id == "2606.00042::00001"
