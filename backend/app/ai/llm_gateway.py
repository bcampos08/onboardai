"""LLM Gateway (Section 3.5): builds a grounded prompt, calls the provider, validates JSON.

It never raises to the QA Controller. Every failure becomes a fallback answer.
"""
import asyncio
import json

from app.ai.llm_provider import LLMProvider
from app.ai.models import GeneratedAnswer, HR_FALLBACK_MESSAGE


def build_prompt(question: str, sections: list) -> str:
    parts = [
        "Answer the employee's question using ONLY the sections below.",
        "If they do not answer it, set fallback to true.",
        'Reply with JSON only: {"answer": str, "cited_section_ids": [str], "fallback": bool}',
        "",
    ]
    for s in sections:
        parts.append(f"[section_id={s.section_id}] {s.title} - {s.heading}")
        parts.append(s.text)
        parts.append("")
    parts.append(f"Question: {question}")
    return "\n".join(parts)


def _fallback(reason: str) -> GeneratedAnswer:
    return GeneratedAnswer(answer=HR_FALLBACK_MESSAGE, fallback=True, fallback_reason=reason)


def validate_output(raw: str, sections: list) -> GeneratedAnswer:
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return _fallback("invalid_output")
    if not isinstance(data, dict) or set(data) != {"answer", "cited_section_ids", "fallback"}:
        return _fallback("invalid_output")
    if not isinstance(data["fallback"], bool) or not isinstance(data["cited_section_ids"], list):
        return _fallback("invalid_output")
    if data["fallback"]:
        return _fallback("no_match")
    allowed = {s.section_id for s in sections}
    cited = data["cited_section_ids"]
    if not cited or any(c not in allowed for c in cited):
        return _fallback("invalid_output")
    if not isinstance(data["answer"], str) or not data["answer"].strip():
        return _fallback("invalid_output")
    return GeneratedAnswer(answer=data["answer"], cited_section_ids=cited)


class LLMGateway:
    def __init__(self, provider: LLMProvider, timeout_seconds: float = 20):
        self.provider = provider
        self.timeout_seconds = timeout_seconds

    async def generate_answer(self, question: str, sections: list) -> GeneratedAnswer:
        prompt = build_prompt(question, sections)
        try:
            raw = await asyncio.wait_for(
                self.provider.generate(prompt, self.timeout_seconds),
                timeout=self.timeout_seconds,
            )
        except asyncio.TimeoutError:
            return _fallback("timeout")
        except Exception:  # provider or network errors; a real client logs these server-side
            return _fallback("provider_error")
        return validate_output(raw, sections)
