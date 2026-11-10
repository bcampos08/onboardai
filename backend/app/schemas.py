"""Request and response models for the REST API (Section 3.4 of the Design Specification)."""
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    conversation_id: Optional[UUID] = None


class CitationOut(BaseModel):
    document_id: str
    section_id: str
    title: str
    section_heading: str
    source_page: Optional[int]


class ChatResultOut(BaseModel):
    conversation_id: str
    message_id: str
    answer: str
    citations: List[CitationOut]
    fallback: bool
    fallback_reason: Optional[Literal["no_match", "timeout", "provider_error", "invalid_output"]]
