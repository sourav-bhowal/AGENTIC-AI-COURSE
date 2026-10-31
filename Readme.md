# Agentic AI Course

Hands-on Python examples for building agentic AI systems — from async fundamentals and data validation with Pydantic, through LangChain ReAct agents (single-agent and multi-agent), to graph-based workflows with LangGraph (sequential, parallel, conditional, iterative, chatbot memory, in-memory / SQLite persistence, tool-calling agents, and RAG over a PDF).

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- Python 3.10+ (uv can install this for you)
- An [OpenAI API key](https://platform.openai.com/api-keys) (modules 03–04; `05` examples 02–03; `06` example 02; `07` example 02; modules 08–13)
- A [Tavily API key](https://tavily.com/) (modules 03–04 and 12)
- A [LangSmith API key](https://smith.langchain.com/) (module 03, to pull the ReAct prompt)

These run without API keys:

- Modules 01 and 02
- `05_langgraph_sequential_agent/01_temp_conversion.py`
- `06_langgraph_parallel_agent/01_employee_analytics.py`
- `07_langgraph_conditional_agent/01_content_moderation.py`

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
| 05 | `05_langgraph_sequential_agent/` | LangGraph sequential graphs — state, LLM nodes, prompt chaining |
| 06 | `06_langgraph_parallel_agent/` | LangGraph parallel fan-out / fan-in — concurrent nodes and reducers |
| 07 | `07_langgraph_conditional_agent/` | LangGraph conditional edges — branch on rules or LLM output |
| 08 | `08_langgraph_iterative_agent/` | LangGraph iterative loops — generate, evaluate, and revise until approved |
| 09 | `09_chatbot_workflow/` | LangGraph chatbot — conversation state, checkpoints, and thread memory |
| 10 | `10_persistence_in_memory/` | LangGraph persistence — `InMemorySaver` checkpoints keyed by `thread_id` |
| 11 | `11_sqlite_persistence/` | LangGraph SQLite persistence — durable `SqliteSaver` checkpoints across restarts |
| 12 | `12_tools_for_agents/` | LangGraph tool-calling agents — `ToolNode`, `tools_condition`, search / weather / calc tools |
| 13 | `13_RAG_using_langgraph/` | RAG with LangGraph — PDF load → chunk → FAISS retrieve → tool-calling chatbot |

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

### 05 — LangGraph sequential

```bash
uv run python 05_langgraph_sequential_agent/01_temp_conversion.py
uv run python 05_langgraph_sequential_agent/02_llm_qa.py
uv run python 05_langgraph_sequential_agent/03_prompt_chaining.py
```

Progresses from a pure-Python graph to LLM nodes and a multi-step prompt chain.

**`01_temp_conversion.py`** — typed state (`celsius` / `fahrenheit` / `weather`), two nodes (`convert_temp` → `weather_report`), `START` → … → `END`, then compile and invoke. No API keys required.

**`02_llm_qa.py`** — a single-node graph that answers a question with `ChatOpenAI` (GPT-4.1-mini). Introduces wiring an LLM into a LangGraph node. Requires `OPENAI_API_KEY`.

**`03_prompt_chaining.py`** — a blog-post pipeline: `generate_outline` → `generate_content` → `evaluate_content`. Shared `BlogPostState` accumulates title, outline, content, and evaluation. Requires `OPENAI_API_KEY`.

### 06 — LangGraph parallel

```bash
uv run python 06_langgraph_parallel_agent/01_employee_analytics.py
uv run python 06_langgraph_parallel_agent/02_ai_essay_analysis.py
```

Shows fan-out from `START` into concurrent nodes, then fan-in to a shared downstream node.

**`01_employee_analytics.py`** — pure-Python parallel graph: `calculate_yearly_salary` and `project_evaluation` run from `START` in parallel, both feed `calculate_bonus`, then `summary`. Interactive CLI prompts for employee inputs. No API keys required.

**`02_ai_essay_analysis.py`** — three LLM evaluators (`evaluate_language`, `evaluate_analysis`, `evaluate_clarity`) run in parallel from `START`, then merge into `evaluate_overall`. Uses structured output (`EvaluationCriteria`) and an `Annotated[list[int], operator.add]` reducer to accumulate scores. Requires `OPENAI_API_KEY`.

### 07 — LangGraph conditional

```bash
uv run python 07_langgraph_conditional_agent/01_content_moderation.py
uv run python 07_langgraph_conditional_agent/02_llm_based_review.py
```

Shows `add_conditional_edges`: a routing function reads state and picks the next node.

**`01_content_moderation.py`** — pure-Python moderation graph. `format_post_content` → `analyze_content`, then a router sends the post to `approve_post`, `flag_for_review` (low user reputation), or `reject_post` (keyword match on hate, violence, sexual, or nudity). Default input is a benign post from a low-reputation user, so it ends as `FLAGGED_FOR_REVIEW`. No API keys required.

**`02_llm_based_review.py`** — an LLM review responder. `find_sentiment` classifies the review as positive or negative with structured output (`SentimentSchema`). A positive review goes to `positive_response` and ends. A negative review goes to `run_diagnosis` (`DiagnosisSchema`: issue type, tone, urgency) and then `negative_response`. Default input is a negative product review. Requires `OPENAI_API_KEY`.

### 08 — LangGraph iterative

```bash
uv run python 08_langgraph_iterative_agent/01_post_approval.py
```

Shows a revise-until-approved loop: a conditional edge routes back to an earlier node until the post is approved or the iteration cap is hit.

**`01_post_approval.py`** — a social-post pipeline. `generate_post` drafts a short post (GPT-4.1-mini), then `evaluate_post` scores it with structured output (`PostEvaluationSchema`: `approved` or `need_improvement`, plus feedback). `check_evaluation` ends the graph when the post is approved or `iteration` reaches `max_iterations`; otherwise it sends the draft to `optimize_post` (GPT-5-mini), which increments the iteration and loops back to `evaluate_post`. `post_history` and `feedback_history` use an `Annotated[list[str], operator.add]` reducer so each pass appends rather than overwrites. Default input is the topic *Make my girlfriend laugh* with `max_iterations` of 3. Requires `OPENAI_API_KEY`.

### 09 — Chatbot workflow

```bash
uv run python 09_chatbot_workflow/01_basic_chatbot.py
```

Shows a conversational LangGraph with persistent turn memory via a checkpointer.

**`01_basic_chatbot.py`** — an interactive CLI chatbot. `ChatState` holds a `messages` list with the `add_messages` reducer so each turn appends rather than overwrites. A single `chat_node` invokes `ChatOpenAI` (GPT-4.1-mini) on the full message history. The graph is compiled with a `MemorySaver` checkpointer and invoked under a fixed `thread_id`, so earlier turns stay in context across the loop. Type `exit` to quit. Requires `OPENAI_API_KEY`.

### 10 — Persistence (in-memory)

```bash
uv run python 10_persistence_in_memory/01_joke.py
```

Shows how a compiled graph saves state between steps when you pass a checkpointer and a thread config.

**`01_joke.py`** — a two-node joke pipeline. `JokeState` holds `topic`, `joke`, and `explanation`. `generate_joke_node` drafts a joke about the topic with `ChatOpenAI` (GPT-4.1-mini), then `explain_joke_node` explains it. The graph is compiled with an `InMemorySaver` checkpointer and invoked with `config={"configurable": {"thread_id": "joke_thread_1"}}`, so the run is stored under that thread. Default topic: *programming with AI*. Requires `OPENAI_API_KEY`.

### 11 — SQLite persistence

```bash
uv run python 11_sqlite_persistence/01_app.py
```

Shows durable conversation memory: checkpoints written to a local SQLite file so history survives process restarts.

**`01_app.py`** — an interactive CLI chatbot backed by `SqliteSaver`. Opens (or creates) `chatbot.db` with `sqlite3.connect(..., check_same_thread=False)`, builds a single-node `chat_node` graph over `ChatState` (`messages` + `add_messages`), and compiles with the SQLite checkpointer. Runs under a fixed `thread_id` (`chat_thread_1`) and streams token chunks via `stream_mode="messages"`. On startup it lists unique thread IDs already stored in the database. Type `exit` to quit. Requires `OPENAI_API_KEY`.

### 12 — Tools for agents

```bash
uv run python 12_tools_for_agents/01_app.py
```

Shows a LangGraph chatbot that can call tools when needed, then loop back to refine the answer.

**`01_app.py`** — an interactive CLI agent with three tools bound to `ChatOpenAI` (GPT-4.1-mini):

- **Tavily Search** (`TavilySearch`) — live web results (`max_results=5`, advanced depth)
- **`get_weather_tool`** — city weather via [wttr.in](https://wttr.in)
- **`calculate_tool`** — safe `eval` of math expressions (`math`, `abs`, `round`, `min`, `max`, `sum`)

The graph has `chat_node` (LLM + bound tools) and a prebuilt `ToolNode`. `tools_condition` routes to `"tools"` when the model requests a tool call, then edges back to `chat_node` so the model can turn tool output into a final reply. Compiled with `InMemorySaver` under `thread_id` `chat_with_tools`. Type `exit` to quit. Requires `OPENAI_API_KEY` and `TAVILY_API_KEY`.

### 13 — RAG using LangGraph

```bash
cd 13_RAG_using_langgraph
uv run python 01_rag.py
```

Shows retrieval-augmented generation: index a PDF into a vector store, then expose retrieval as a tool the chatbot can call.

**`01_rag.py`** — an interactive CLI RAG chatbot over `resume.pdf`. Pipeline:

1. **Load** — `PyPDFLoader` reads the PDF
2. **Chunk** — `RecursiveCharacterTextSplitter` (`chunk_size=1000`, `chunk_overlap=200`)
3. **Embed & index** — `OpenAIEmbeddings` (`text-embedding-3-small`) + `FAISS.from_documents`
4. **Retrieve** — similarity search with `k=4`
5. **Chat** — LangGraph tool-calling loop: `chat_node` (GPT-4.1-mini + bound tools) ↔ `ToolNode` via `tools_condition`

The `search_resume` tool queries the FAISS retriever and returns formatted chunks (source, page, content). Run from `13_RAG_using_langgraph/` so `resume.pdf` resolves. Type `exit` to quit. Requires `OPENAI_API_KEY`.

## Dependencies

Key packages (see `requirements.txt` for the full list):

- `langchain`, `langchain-openai`, `langchain-community`, `langchainhub`, `langchain-tavily`, `langchain-text-splitters`
- `langgraph`, `langgraph-checkpoint-sqlite`
- `langsmith`
- `faiss-cpu`, `pypdf`
- `pydantic`
- `tavily-python`
- `trafilatura`, `readability-lxml`, `beautifulsoup4`
- `requests`
- `python-dotenv`

## Notes

- Keep `.env` out of version control (already listed in `.gitignore`).
- The single agent uses the [LangSmith](https://smith.langchain.com/) client to pull the ReAct prompt (`hwchase17/react`).
- Module 05 covers linear graphs (state + nodes + edges). Module 06 adds parallel fan-out / fan-in and reducers. Module 07 adds conditional branching with `add_conditional_edges`. Module 08 adds an iterative loop that routes back to an earlier node until a stop condition. Module 09 adds a conversational chatbot with `add_messages` and `MemorySaver` thread checkpoints. Module 10 saves a multi-node run with `InMemorySaver` under a `thread_id`. Module 11 persists chatbot checkpoints to SQLite with `SqliteSaver` so memory survives restarts. Module 12 adds tool calling with `ToolNode` and `tools_condition` (search, weather, and calculator). Module 13 adds RAG: PDF → chunks → FAISS embeddings → retrieve-as-tool chatbot.
