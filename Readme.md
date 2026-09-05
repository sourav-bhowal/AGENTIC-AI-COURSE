# Agentic AI Course

Hands-on Python examples for building agentic AI systems — from async fundamentals and data validation with Pydantic to a LangChain ReAct agent with web search and custom tools.

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- Python 3.10+ (uv can install this for you)
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A [Tavily API key](https://tavily.com/) (for the LangChain agent module)

## Setup

```bash
# Clone the repo
git clone https://github.com/sourav-bhowal/AGENTIC-AI-COURSE.git
cd AGENTIC-AI-COURSE

# Create a virtual environment
uv venv

# Install dependencies
uv pip install -r requirements.txt
```

### Environment variables

Copy the sample env file and add your keys:

```bash
# Windows
copy .env.sample .env

# macOS / Linux
cp .env.sample .env
```

Then edit `.env`:

```
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

## Course structure

| Module | Folder | What you'll learn |
|--------|--------|-------------------|
| 01 | `01_async_sync_concept/` | Sync vs async I/O — why agents benefit from concurrency |
| 02 | `02_pydantic_for_agent/` | Data validation with Pydantic — models agents can trust |
| 03 | `03_langchain_agent/` | LangChain ReAct agent with Tavily search and a custom weather tool |

### 01 — Async / Sync

```bash
uv run python 01_async_sync_concept/01_sync_code.py
uv run python 01_async_sync_concept/02_async_code.py
```

Compares sequential (blocking) vs concurrent async data fetching.

### 02 — Pydantic for agents

```bash
uv run python 02_pydantic_for_agent/01_without_pydantic.py
uv run python 02_pydantic_for_agent/02_with_pydantic.py
uv run python 02_pydantic_for_agent/03_advance_pydantic.py
uv run python 02_pydantic_for_agent/04_complex_pydantic.py
uv run python 02_pydantic_for_agent/05_nested_models_pydantic.py
```

Progresses from plain dicts to validated, nested Pydantic models.

### 03 — LangChain agent

```bash
uv run python 03_langchain_agent/01_single_agent.py
```

Builds a ReAct agent (GPT-4.1-mini) that combines:

- **Tavily Search** — live web results for news and current events
- **Custom `get_weather` tool** — city weather via [wttr.in](https://wttr.in)

Requires both API keys in `.env`. Run with `verbose=True` to see the agent's reasoning and which tools it chooses.

## Dependencies

Key packages (see `requirements.txt` for the full list):

- `langchain`, `langchain-openai`, `langchain-community`, `langchainhub`
- `pydantic`
- `tavily-python`
- `requests`
- `python-dotenv`

## Notes

- Keep `.env` out of version control (already listed in `.gitignore`).
- The LangChain agent pulls the ReAct prompt from [LangChain Hub](https://smith.langchain.com/hub/hwchase17/react) (`hwchase17/react`).
