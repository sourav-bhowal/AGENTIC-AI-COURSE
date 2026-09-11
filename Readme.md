# Agentic AI Course

Hands-on Python examples for building agentic AI systems — from async fundamentals and data validation with Pydantic, through LangChain ReAct agents (single-agent and multi-agent), to graph-based workflows with LangGraph.

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- Python 3.10+ (uv can install this for you)
- An [OpenAI API key](https://platform.openai.com/api-keys) (modules 03–04)
- A [Tavily API key](https://tavily.com/) (modules 03–04)
- A [LangSmith API key](https://smith.langchain.com/) (module 03, to pull the ReAct prompt)

Modules 01, 02, and 05 run without API keys.

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
| 04 | `04_langchain_multi_agent/` | Multi-agent research pipeline — search, scrape, write, critique |
| 05 | `05_langgraph_agent/` | LangGraph — state, nodes, edges, and compiling a graph |

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

A sequential research pipeline with four stages:

1. **Search agent** — Tavily web search for a topic
2. **Reader agent** — scrapes the most relevant URLs (trafilatura → readability → BeautifulSoup fallback)
3. **Writer chain** — drafts a structured research report
4. **Critic chain** — scores the report and lists strengths / areas to improve

Default topic: *The impact of AI on the future of work*. Requires `OPENAI_API_KEY` and `TAVILY_API_KEY`.

```
04_langchain_multi_agent/
├── app.py                 # Entry point
└── src/
    ├── agents/            # Search, reader, writer, critic
    ├── tools/             # web_search and web_scrape
    └── pipelines/         # Orchestration and routing
```

### 05 — LangGraph

```bash
uv run python 05_langgraph_agent/01_temp_conversion.py
```

**`01_temp_conversion.py`** — a minimal LangGraph workflow: typed state (`celsius` / `fahrenheit`), a conversion node, `START` → node → `END` edges, then compile and invoke. No API keys required.

## Dependencies

Key packages (see `requirements.txt` for the full list):

- `langchain`, `langchain-openai`, `langchain-community`, `langchainhub`
- `langgraph`
- `langsmith`
- `pydantic`
- `tavily-python`
- `trafilatura`, `readability-lxml`, `beautifulsoup4`
- `requests`
- `python-dotenv`

## Notes

- Keep `.env` out of version control (already listed in `.gitignore`).
- The single agent uses the [LangSmith](https://smith.langchain.com/) client to pull the ReAct prompt (`hwchase17/react`).
- Module 05 is a first LangGraph example (state + a single node). Later examples will add branching, loops, and tool-calling graphs.
