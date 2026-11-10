from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.routers import chat

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(title="OnboardAI API", version="0.1.0")
app.include_router(chat.router)


@app.get("/", include_in_schema=False)
def demo_page() -> FileResponse:
    """Simple demo chat page. Temporary until the React frontend is built."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}
