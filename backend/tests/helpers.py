"""Small test doubles shared by the test files."""
import asyncio


class FixedLLM:
    """Returns whatever text it is given, so tests can check validation."""

    def __init__(self, text: str):
        self.text = text
        self.calls = 0

    async def generate(self, prompt: str, timeout_seconds: float = 20) -> str:
        self.calls += 1
        return self.text


class SlowLLM:
    async def generate(self, prompt: str, timeout_seconds: float = 20) -> str:
        await asyncio.sleep(5)
        return "{}"


class BrokenLLM:
    async def generate(self, prompt: str, timeout_seconds: float = 20) -> str:
        raise ConnectionError("provider unavailable")
