"""LLMProvider interface (Section 3.5). RealLLMClient and MockLLM both implement it."""
import json
from typing import Protocol


class LLMProvider(Protocol):
    async def generate(self, prompt: str, timeout_seconds: float = 20) -> str: ...


class MockLLM:
    """Sprint 1 stand-in for the real model. No API key or internet needed.

    It answers by quoting the best-matching section from the prompt. A real LLM
    would write a natural answer instead, but the JSON format is identical.
    """

    async def generate(self, prompt: str, timeout_seconds: float = 20) -> str:
        lines = prompt.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("[section_id="):
                section_id = line[len("[section_id="):].split("]")[0]
                source = line.split("] ", 1)[1] if "] " in line else "the handbook"
                text = lines[i + 1] if i + 1 < len(lines) else ""
                return json.dumps({
                    "answer": f"According to the {source}: {text}",
                    "cited_section_ids": [section_id],
                    "fallback": False,
                })
        return json.dumps({"answer": "", "cited_section_ids": [], "fallback": True})


# TODO (Sprint 2): add RealLLMClient here. It must read its API key from the
# environment and must never log the key or the full prompt.
