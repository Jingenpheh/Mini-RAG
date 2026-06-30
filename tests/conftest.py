"""Shared pytest fixtures for tests/unit/.

The fake DoclingDocument helpers let chunking tests run without parsing a
real PDF. The fakes do not subclass the real Docling classes. Instead,
install_docling_class_fakes monkeypatches the module-level class names in
docling_core.types.doc.document to point at the fakes. The chunker imports
from that module inside chunk_document() at call time, so isinstance() checks
resolve to the fakes for the duration of the test.
"""

import pytest
from docling_core.types.doc.document import (
    FormulaItem,
    SectionHeaderItem,
    TableItem,
    TextItem,
    TitleItem,
)


class _FakeLabel:
    def __init__(self, value: str):
        self.value = value


class FakeTextItem:
    """Duck-typed fake TextItem with .text and .label.value attributes."""

    def __init__(self, text: str, label: str = "text"):
        self.text = text
        self.label = _FakeLabel(label)


class FakeSectionHeader:
    """Duck of SectionHeaderItem."""

    def __init__(self, text: str):
        self.text = text


class FakeFormulaItem:
    """Duck of FormulaItem. Carries both .text and .orig like the real class."""

    def __init__(self, text: str = "", orig: str = ""):
        self.text = text
        self.orig = orig


class FakeTableItem:
    """Duck of TableItem with a fixed markdown payload."""

    def __init__(self, markdown: str):
        self._markdown = markdown

    def export_to_markdown(self, doc) -> str:  # noqa: ARG002 (matches real signature)
        return self._markdown


class _FakeDoc:
    def __init__(self, items: list):
        self._items = items

    def iterate_items(self, with_groups: bool = False):  # noqa: ARG002
        return [(item, 0) for item in self._items]


def fake_doc(items: list) -> _FakeDoc:
    """Build a fake DoclingDocument from a list of items."""
    return _FakeDoc(items)


@pytest.fixture
def install_docling_class_fakes(monkeypatch):
    """Patch docling's class names so the chunker's isinstance checks see fakes.

    chunk_document() does `from docling_core.types.doc.document import ...`
    inside the function body. Each time chunk_document() runs, that import
    re-resolves the names from the module dict. monkeypatch.setattr replaces
    the module-level names with the fakes for the test's duration, so the
    chunker's isinstance checks see the fakes as the relevant classes.
    """
    import docling_core.types.doc.document as ddoc

    monkeypatch.setattr(ddoc, "TextItem", FakeTextItem)
    monkeypatch.setattr(ddoc, "SectionHeaderItem", FakeSectionHeader)
    monkeypatch.setattr(ddoc, "FormulaItem", FakeFormulaItem)
    monkeypatch.setattr(ddoc, "TableItem", FakeTableItem)
    monkeypatch.setattr(ddoc, "TitleItem", FakeTextItem)  # not used directly; alias is fine
    yield
