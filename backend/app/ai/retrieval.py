"""Placeholder RetrievalService until ChromaDB and the Embedding Client are added.

Scores sections by simple word overlap so the pipeline can be tested end to end.
Replace with vector search in Sprint 2; the search() signature must not change.

The sample sections come from backend/sample_data/handbook.json (a made-up company).
"""
import json
import re
from dataclasses import replace
from pathlib import Path

from app.ai.models import RetrievedSection

HANDBOOK_PATH = Path(__file__).resolve().parents[2] / "sample_data" / "handbook.json"

_WORD = re.compile(r"[a-z0-9]+")
_STOP = {
    "a", "an", "the", "i", "me", "my", "we", "our", "you", "your", "it", "this", "that",
    "do", "does", "did", "is", "are", "am", "be", "can", "will", "should", "would",
    "how", "what", "when", "where", "who", "why", "which", "there", "any",
    "to", "of", "for", "in", "on", "at", "by", "with", "about", "from", "and", "or",
    "get", "have", "has",
}


def _stem(word: str) -> str:
    return word[:-1] if len(word) > 3 and word.endswith("s") else word


def _words(text: str) -> set:
    return {_stem(w) for w in _WORD.findall(text.lower()) if w not in _STOP}


def load_sections(path: Path = HANDBOOK_PATH) -> list:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [RetrievedSection(**s, similarity=0.0) for s in data["sections"]]


class InMemoryRetrievalService:
    def __init__(self, sections: list):
        self.sections = sections

    async def search(self, query: str, top_k: int = 5) -> list:
        q = _words(query)
        if not q:
            return []
        scored = []
        for s in self.sections:
            overlap = len(q & _words(s.heading + " " + s.text)) / len(q)
            if overlap > 0:
                scored.append(replace(s, similarity=round(overlap, 3)))
        scored.sort(key=lambda r: r.similarity, reverse=True)
        return scored[:top_k]


SAMPLE_SECTIONS = load_sections()
