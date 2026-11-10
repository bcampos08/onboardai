# OnboardAI

An AI assistant that answers employee questions from approved company documents, cites its sources, and sends questions it cannot answer to HR.

**Stack:** React · Python FastAPI · PostgreSQL · ChromaDB · hosted LLM with retrieval-augmented generation (RAG)

**Team:** Brad Campos (Lead Architect), Jared Ahenkora-Kwakyi (Interface Designer), Muhammed Ayday (Integration Lead)

## Try the demo (easiest way)

You only need **Python 3.12** installed (from python.org/downloads; on Windows, check **"Add python.exe to PATH"** in the installer). Then:

- **Windows:** double-click **`Start OnboardAI (Windows).bat`**
- **Mac:** double-click **`Start OnboardAI (Mac).command`**

The first start takes a minute or two to set things up. Your browser then opens the OnboardAI chat page at http://localhost:8000. Keep the black window open while you use it, and close it to stop the app.

**Mac notes:** if macOS says the file can't be opened because it's from an unidentified developer, right-click the file, choose **Open**, then **Open** again. If it says you don't have permission, open the Terminal app, type `bash ` (with a space), drag the file into the window, and press Enter.

**Windows note:** if a blue "Windows protected your PC" box appears, click **More info**, then **Run anyway**.

### Where the answers come from

Right now, answers come from `backend/sample_data/handbook.json`: ten short sections from a **made-up company handbook** (Brightpath Inc.), covering time off, dress code, work hours, remote work, health insurance, retirement, laptop setup, passwords, pay schedule, and direct deposit. Questions about anything else, like parking, get the "contact HR" fallback.

A stand-in **mock AI** quotes the best-matching section instead of writing its own answer, so the demo needs no API key or internet. You can add or edit sections in `handbook.json` without touching any code; restart the app to see changes.

## Repository layout

```
backend/            FastAPI app
  app/ai/           AI Chatbot Module: QA Controller, LLM Gateway, MockLLM, retrieval
  app/routers/      REST endpoints
  app/static/       Demo chat page (temporary, until the React frontend exists)
  sample_data/      Made-up company handbook used by the demo and tests
  tests/            pytest tests (run automatically on every pull request)
frontend/           React app (not created yet; see frontend/README.md)
docs/               Design Specification and architecture diagram
.github/            CI workflow, pull request and issue templates, code owners
```

## Run the backend from a terminal (for developers)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                           # run the tests
uvicorn app.main:app --reload    # chat page at http://localhost:8000, API docs at /docs
```

The current backend is the Sprint 1 version: `POST /api/chat/ask` works end to end using **MockLLM** and the sample handbook, so the frontend can be built against the real response format before the hosted LLM and real document uploads are connected.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before your first pull request. In short: work on a feature branch, open a pull request, get one teammate's approval, and make sure the tests pass. AI-generated code follows the same rules, plus disclosure in the pull request.
