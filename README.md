# Autonomous Market Research Agent

**Multi-agent LLM system that decomposes a research topic into parallel subqueries and synthesizes a structured 2-3 page report in under 60 seconds.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-multi--agent-green)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Overview

Most LLM research tools are single-pass wrappers: one prompt in, one answer out. This system uses a stateful 3-agent pipeline where a Planner breaks the topic into specific research questions, independent Researcher agents query the web in parallel, and a Writer synthesizes everything into a structured report with an executive summary.

The result: deeper coverage, better source diversity, and faster completion than sequential single-agent approaches.

---

## Architecture

```
Input Topic
     │
     ▼
┌──────────┐
│  Planner │  Decomposes topic into 3-5 specific research questions
└──────────┘
     │
     ▼ (parallel)
┌────────────┐  ┌────────────┐  ┌────────────┐
│ Researcher │  │ Researcher │  │ Researcher │  Each handles one subquery
│   Agent 1  │  │   Agent 2  │  │   Agent N  │  Web search + synthesis
└────────────┘  └────────────┘  └────────────┘
     │               │               │
     └───────────────┴───────────────┘
                     │
                     ▼
              ┌────────────┐
              │   Writer   │  Combines findings into structured markdown report
              └────────────┘
                     │
                     ▼
           Structured Research Report
           (Executive Summary + Sections + Key Takeaways)
```

**State management:** LangGraph handles the agent graph, state transitions, and parallel execution. Each agent's output is passed downstream as typed state.

---

## Stack

| Component | Technology |
|-----------|-----------|
| Agent orchestration | LangGraph |
| LLM inference | Groq (Llama 3.3 70B) |
| Web search | DuckDuckGo Search API |
| Output format | Structured markdown |
| Language | Python 3.10+ |

---

## Quick Start

```bash
git clone https://github.com/nishat123456/market-research-agent
cd market-research-agent
python -m venv venv && source venv/activate
pip install -r requirements.txt
cp .env.example .env  # add your GROQ_API_KEY
```

```bash
# Run with a topic
python main.py "Retrieval-Augmented Generation in enterprise software 2025"

# Interactive mode
python main.py
```

Get a free Groq API key at [console.groq.com](https://console.groq.com).

---

## Example Output Structure

```
# Electric Vehicle Market in Southeast Asia

## Executive Summary
...

## Market Size and Growth Trends
...

## Key Players and Competitive Landscape
...

## Infrastructure and Policy Environment
...

## Key Takeaways
1. ...
2. ...
3. ...
```

---

## Design Decisions

**Why LangGraph over a simple loop?** Stateful graph execution lets each agent pass structured typed output to the next stage rather than raw strings. This makes the pipeline composable and the state inspectable at each node.

**Why Groq?** Sub-second inference on Llama 3.3 70B keeps the full pipeline under 60 seconds even with parallel subquery execution.

**Why DuckDuckGo?** No API key required, no rate limit for moderate use, and sufficient for research-grade source diversity.

---

**Author:** Mustaqim Nishat | [nishat12sikdar@gmail.com](mailto:nishat12sikdar@gmail.com)
