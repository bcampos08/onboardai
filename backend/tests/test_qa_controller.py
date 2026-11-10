"""QA Controller behavior (Section 3.5)."""
import asyncio
import json

from app.ai.llm_gateway import LLMGateway
from app.ai.llm_provider import MockLLM
from app.ai.qa_controller import QAController
from app.ai.retrieval import InMemoryRetrievalService, SAMPLE_SECTIONS
from tests.helpers import FixedLLM


def make_controller(provider):
    return QAController(InMemoryRetrievalService(SAMPLE_SECTIONS), LLMGateway(provider), relevance_threshold=0.5)


def test_unrelated_question_returns_no_match_without_calling_llm():
    llm = FixedLLM(json.dumps({"answer": "x", "cited_section_ids": ["sec-001"], "fallback": False}))
    result = asyncio.run(make_controller(llm).answer("What is the parking policy?", "u1", None))
    assert (result.fallback, result.fallback_reason) == (True, "no_match")
    assert result.citations == []
    assert llm.calls == 0


def test_matching_question_returns_cited_answer():
    result = asyncio.run(make_controller(MockLLM()).answer("How do I request time off?", "u1", None))
    assert result.fallback is False
    assert result.citations[0].section_id == "sec-001"
    assert result.citations[0].section_heading == "Time Off"


def test_sample_handbook_loads():
    assert len(SAMPLE_SECTIONS) >= 10
    assert len({s.section_id for s in SAMPLE_SECTIONS}) == len(SAMPLE_SECTIONS)
