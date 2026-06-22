# ##############################################################################
# File: pii.py
# Purpose: PII detection and scrubbing stage. Currently a passthrough; the slot
#          exists so the call site is in the right place when real detection
#          gets wired up.
#
# Contents:
#   Functions:
#     scrub_pii()           - Detect and redact PII from parsed text (stub)
# ##############################################################################


# Standard library
from typing import Optional


# ##############################################################################
# PII scrubbing
# ##############################################################################


def scrub_pii(parsed_text: str, paper_meta: Optional[dict] = None) -> str:
    """Detect and redact PII from parsed document text.

    Args:
        parsed_text (str): The text returned by the parser.
        paper_meta (Optional[dict]): Manifest metadata for the paper.

    Approach:
        Currently a passthrough that returns the input unchanged. The intended
        implementation uses Microsoft Presidio (regex + spaCy NER, no LLM
        calls) to detect entities such as addresses, personal emails, dates of
        birth, and credit card numbers, then redact them.

        For the arXiv corpus there's nothing meaningful to detect. Author names
        and affiliations are deliberately public and must NOT be redacted, so
        any production version of this function would need an entity allowlist
        scoped to the document type.

        The slot exists between QC and chunking so that any redaction happens
        before content gets split into chunks. Otherwise the same PII could
        leak across chunk boundaries.

    Returns:
        str: The (possibly redacted) text. Currently identical to the input.
    """
    return parsed_text
