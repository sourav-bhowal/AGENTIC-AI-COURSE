# Agentic AI Course

Hands-on Python examples for building agentic AI systems — from async fundamentals and data validation with Pydantic to LangChain ReAct agents (single-agent and multi-agent).

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- Python 3.10+ (uv can install this for you)
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A [Tavily API key](https://tavily.com/) (for the LangChain agent modules)
- A [LangSmith API key](https://smith.langchain.com/) (to pull the ReAct prompt)

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
LANGSMITH_API_KEY=your_langsmith_key
```

## Course structure

| Module | Folder | What you'll learn |
|--------|--------|-------------------|
| 01 | `01_async_sync_concept/` | Sync vs async I/O — why agents benefit from concurrency |
| 02 | `02_pydantic_for_agent/` | Data validation with Pydantic — models agents can trust |
| 03 | `03_langchain_single_agent/` | LangChain ReAct single agent — tools + web search |
| 04 | `04_langchain_multi_agent/` | Multi-agent pipelines — agents, tools, and orchestration |

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

### 03 — LangChain single agent

```bash
uv run python 03_langchain_single_agent/01_single_agent.py
```

**`01_single_agent.py`** — a ReAct agent (GPT-4.1-mini) that combines:

- **Tavily Search** — live web results for news and current events
- **Custom `get_weather` tool** — city weather via [wttr.in](https://wttr.in)

Requires all three API keys in `.env`. The ReAct prompt is pulled from LangSmith (`hwchase17/react`). Run with `verbose=True` to see the agent's reasoning and which tools it chooses.

### 04 — LangChain multi-agent

```bash
uv run python 04_langchain_multi_agent/app.py
```

Scaffolded layout for a multi-agent system:

```
04_langchain_multi_agent/
├── app.py                 # Entry point
└── src/
    ├── agents/            # Agent definitions
    ├── tools/             # Shared / agent-specific tools
    └── pipelines/         # Orchestration and routing
```

Implementation is in progress.

## Dependencies

Key packages (see `requirements.txt` for the full list):

- `langchain`, `langchain-openai`, `langchain-community`, `langchainhub`
- `langsmith`
- `pydantic`
- `tavily-python`
- `requests`
- `python-dotenv`

## Notes

- Keep `.env` out of version control (already listed in `.gitignore`).
- The single agent uses the [LangSmith](https://smith.langchain.com/) client to pull the ReAct prompt (`hwchase17/react`).
