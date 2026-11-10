"""Chat API: POST /api/chat/ask (Section 3.4).

Sprint 1 version: uses MockLLM and sample sections, and does not check login tokens yet.
"""
from dataclasses import asdict

from fastapi import APIRouter, Depends

from app import config
from app.ai.llm_gateway import LLMGateway
from app.ai.llm_provider import MockLLM
from app.ai.qa_controller import QAController
from app.ai.retrieval import InMemoryRetrievalService, SAMPLE_SECTIONS
from app.schemas import AskRequest, ChatResultOut

router = APIRouter(prefix="/api/chat", tags=["chat"])


def get_qa_controller() -> QAController:
    return QAController(
        retrieval=InMemoryRetrievalService(SAMPLE_SECTIONS),
        gateway=LLMGateway(MockLLM(), timeout_seconds=config.LLM_TIMEOUT_SECONDS),
        relevance_threshold=config.RELEVANCE_THRESHOLD,
        top_k=config.TOP_K,
    )


@router.post("/ask", response_model=ChatResultOut)
async def ask(body: AskRequest, qa: QAController = Depends(get_qa_controller)) -> ChatResultOut:
    # TODO: replace with the user from AuthService.verify_token() once login exists.
    user_id = "demo-user"
    conversation_id = str(body.conversation_id) if body.conversation_id else None
    result = await qa.answer(body.question, user_id, conversation_id)
    return ChatResultOut(**asdict(result))
