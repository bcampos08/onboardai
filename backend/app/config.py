"""Settings read from environment variables. Copy .env.example to .env for local runs."""
import os

RELEVANCE_THRESHOLD = float(os.getenv("RELEVANCE_THRESHOLD", "0.5"))
LLM_TIMEOUT_SECONDS = float(os.getenv("LLM_TIMEOUT_SECONDS", "20"))
TOP_K = int(os.getenv("TOP_K", "5"))
