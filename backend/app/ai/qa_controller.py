"""QA Controller (Section 3.5): the only entry point into the AI module."""
import uuid
from typing import Optional

from app.ai.llm_gateway import LLMGateway
from app.ai.models import ChatResult, Citation, HR_FALLBACK_MESSAGE


class QAController:
    def __init__(self, retrieval, gateway: LLMGateway, relevance_threshold: float, top_k: int = 5):
        self.retrieval = retrieval
        self.gateway = gateway
        self.relevance_threshold = relevance_threshold
        self.top_k = top_k

    async def answer(self, question: str, user_id: str, conversation_id: Optional[str]) -> ChatResult:
        conversation_id = conversation_id or str(uuid.uuid4())
        message_id = str(uuid.uuid4())

        sections = await self.retrieval.search(question, top_k=self.top_k)
        if not sections or max(s.similarity for s in sections) < self.relevance_threshold:
            # Below the relevance threshold: skip the LLM entirely.
            return ChatResult(conversation_id, message_id, HR_FALLBACK_MESSAGE, [], True, "no_match")

        generated = await self.gateway.generate_answer(question, sections)
        if generated.fallback:
            return ChatResult(conversation_id, message_id, generated.answer, [],
                              True, generated.fallback_reason)

        by_id = {s.section_id: s for s in sections}
        citations = [
            Citation(s.document_id, s.section_id, s.title, s.heading, s.source_page)
            for s in (by_id[c] for c in generated.cited_section_ids)
        ]
        # TODO: call LoggingService.record_chat(user_id, question, result) once the database exists.
        return ChatResult(conversation_id, message_id, generated.answer, citations, False, None)
