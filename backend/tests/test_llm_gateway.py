"""LLM Gateway must turn every bad outcome into an HR fallback (Section 3.5)."""
import asyncio
import json

from app.ai.llm_gateway import LLMGateway
from app.ai.retrieval import SAMPLE_SECTIONS
from tests.helpers import BrokenLLM, FixedLLM, SlowLLM


def run(gateway):
    return asyncio.run(gateway.generate_answer("How do I request time off?", SAMPLE_SECTIONS))


def test_valid_output_is_accepted():
    raw = json.dumps({"answer": "Use the HR portal.", "cited_section_ids": ["sec-001"], "fallback": False})
    result = run(LLMGateway(FixedLLM(raw)))
    assert result.fallback is False
    assert result.cited_section_ids == ["sec-001"]


def test_non_json_output_falls_back():
    result = run(LLMGateway(FixedLLM("Sure! Here is your answer.")))
    assert (result.fallback, result.fallback_reason) == (True, "invalid_output")


def test_citing_a_section_that_was_not_retrieved_falls_back():
    raw = json.dumps({"answer": "Made up.", "cited_section_ids": ["sec-999"], "fallback": False})
    result = run(LLMGateway(FixedLLM(raw)))
    assert (result.fallback, result.fallback_reason) == (True, "invalid_output")


def test_timeout_falls_back():
    result = run(LLMGateway(SlowLLM(), timeout_seconds=0.1))
    assert (result.fallback, result.fallback_reason) == (True, "timeout")


def test_provider_error_falls_back():
    result = run(LLMGateway(BrokenLLM()))
    assert (result.fallback, result.fallback_reason) == (True, "provider_error")
