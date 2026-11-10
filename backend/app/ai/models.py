"""Data contracts from Section 3.6 of the Design Specification.

Plain dataclasses keep the AI module independent of FastAPI.
Field names here must match the interface contracts exactly.
"""
from dataclasses import dataclass, field
from typing import Optional

FALLBACK_REASONS = {"no_match", "timeout", "provider_error", "invalid_output"}

HR_FALLBACK_MESSAGE = (
    "I couldn't find this in the approved documents. "
    "Please contact HR or select Send to HR."
)


@dataclass
class RetrievedSection:
    section_id: str
    document_id: str
    title: str
    heading: str
    text: str
    source_page: Optional[int]
    similarity: float  # 0 to 1


@dataclass
class GeneratedAnswer:
    answer: str
    cited_section_ids: list = field(default_factory=list)
    fallback: bool = False
    fallback_reason: Optional[str] = None


@dataclass
class Citation:
    document_id: str
    section_id: str
    title: str
    section_heading: str
    source_page: Optional[int]


@dataclass
class ChatResult:
    conversation_id: str
    message_id: str
    answer: str
    citations: list
    fallback: bool
    fallback_reason: Optional[str]
