# 🔬 Autonomous Market Research Agent

A multi-agent system that automates deep-dive market analysis using LangGraph for stateful task orchestration.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-green)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)

## Overview

This tool takes a research topic and automatically:
1. **Plans** - Breaks down the topic into specific research questions
2. **Researches** - Searches the web and analyzes results for each question
3. **Synthesizes** - Compiles findings into a structured research report

### Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Planner   │────▶│  Researcher  │────▶│   Writer    │
│    Agent    │     │    Agent     │     │    Agent    │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │  Web Search │
                    │    Tools    │
                    └─────────────┘
```

## Features

- **Multi-Agent Orchestration**: Uses LangGraph for stateful workflow management
- **Autonomous Research**: Generates sub-questions and researches each independently
- **Web Search Integration**: Real-time data gathering via DuckDuckGo
- **Structured Reports**: Outputs professional markdown reports with executive summaries

## Installation

```bash
# Clone the repository
git clone https://github.com/nishat123456/market-research-agent.git
cd market-research-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

## Getting a Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys
4. Create a new key and copy it to your `.env` file

## Usage

### Command Line

```bash
# With topic as argument
python main.py "Electric vehicle market in Southeast Asia"

# Interactive mode
python main.py
```

### Example Output

```
🚀 Starting Market Research Agent
📌 Topic: Electric vehicle market in Southeast Asia

🎯 Planning research for: Electric vehicle market in Southeast Asia
📋 Generated 5 research questions
   1. What is the current market size and growth rate of EVs in Southeast Asia?
   2. Which countries have the highest adoption rates?
   ...

🔍 Researching (1/5): What is the current market size...
   Found 8 sources

✍️  Writing final report...
✅ Report complete!

💾 Report saved to: outputs/Electric_vehicle_market_20240202_143022.md
```

## Project Structure

```
market-research-agent/
├── main.py          # Entry point and CLI
├── agents.py        # Agent definitions (Planner, Researcher, Writer)
├── graph.py         # LangGraph workflow orchestration
├── tools.py         # Web search tools
├── requirements.txt # Dependencies
├── .env.example     # Environment template
└── outputs/         # Generated reports
```

## Tech Stack

- **Python 3.10+**
- **LangGraph** - Multi-agent workflow orchestration
- **LangChain** - LLM framework
- **Groq** - Fast LLM inference (Llama 3.3 70B)
- **DuckDuckGo Search** - Free web search API

## How It Works

1. **Planning Phase**: The Planner agent analyzes the input topic and generates 3-5 specific research questions that will comprehensively cover the subject.

2. **Research Phase**: For each question, the Researcher agent:
   - Performs web searches using DuckDuckGo
   - Analyzes and synthesizes the search results
   - Extracts key insights with citations

3. **Writing Phase**: The Writer agent takes all findings and produces a structured report with:
   - Executive summary
   - Key findings organized by theme
   - Conclusion and future outlook

## License

MIT

## Author

M M Nishat - [GitHub](https://github.com/nishat123456)
