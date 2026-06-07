"""
Tier 0 — Grounded reading layer.

Two responsibilities, both deterministic:
  facts.py      build the canonical fact-table + grounding payload from a chart
  validator.py  diff an LLM-generated reading against that fact-table

Architecture (hybrid): engine -> fact-table -> LLM (style only) -> validator -> PDF.
The LLM is never the source of an astrological claim; it only rephrases facts
it is handed. The validator is the backstop that catches any drift.
"""
from .facts import build_fact_table, grounding_text
from .validator import validate_reading, Violation
from .template import (
    SECTIONS, Section, build_reading_plan, section_grounding, MASS, DEEP,
)

__all__ = [
    "build_fact_table", "grounding_text", "validate_reading", "Violation",
    "SECTIONS", "Section", "build_reading_plan", "section_grounding", "MASS", "DEEP",
]
