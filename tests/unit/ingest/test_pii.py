"""Placeholder. mini_rag/ingest/pii.py::scrub_pii is currently a passthrough
stub with no implementation logic to pin.

When the Presidio integration lands, add tests here for:
  - Email / address / DOB redaction behavior on text containing PII.
  - The author-name allowlist that prevents scrubbing public arXiv author
    names and affiliations (the docstring on scrub_pii spells this out).
  - The passthrough fallback when paper_meta is missing or empty.

Leaving this file empty is deliberate. A test that just asserts
`scrub_pii(text) == text` only pins the stub, and that "test" has to be
rewritten the moment Presidio gets wired in, so it's not catching a
regression at that point. The file's presence is a placeholder, nothing
more.
"""
