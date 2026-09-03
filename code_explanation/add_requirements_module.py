import os
import json

from build_all_modules_complete import build_all_data

modules = build_all_data()

# Read the previous grounding module
from add_grounding_masterclass import grounding_module

requirements_module = {
    "id": "requirements-guide",
    "category": "10. Factual Grounding & Dependencies",
    "badge": "Dependencies",
    "badgeColor": "slate",
    "title": "Python Dependencies & Technology Stack (requirements.txt)",
    "path": "requirements.txt",
    "summary": "This file lists all the third-party Python packages and libraries required to run FinAgent. Think of it like a master ingredients list for a recipe. When you run 'pip install -r requirements.txt', Python automatically downloads and installs these packages so your LangGraph agents, ChromaDB vector store, FastAPI server, and Streamlit UI work seamlessly.",
    "keyConcepts": [
        "pip Package Manager",
        "Version Pinning (>=)",
        "Virtual Environments (.venv)",
        "LangChain & LangGraph Ecosystem",
        "Pydantic v2 Type Validation",
        "ChromaDB & Rank-BM25 Search",
        "FastAPI & Uvicorn Async Server",
        "Streamlit Dashboard"
    ],
    "interviewQuestions": [
        {
            "question": "Can you walk through the core third-party dependencies in your requirements.txt?",
            "answer": "Our tech stack is structured into 6 modular layers: 1) LangGraph & LangChain for cyclical multi-agent orchestration and text splitting; 2) Pydantic v2 for strict state validation; 3) ChromaDB and rank-bm25 for Dense-Sparse Hybrid RAG; 4) Ragas and Pytest for LLM-as-a-Judge automated evaluation; 5) FastAPI and Uvicorn for asynchronous backend microservices; and 6) Streamlit for analyst dashboards."
        },
        {
            "question": "Why do you use '>=' version constraints in requirements.txt?",
            "answer": "Version constraints like 'langgraph>=0.2.14' ensure minimum feature compatibility while allowing non-breaking security patches to be installed. In production container builds, we lock dependencies to ensure reproducible builds across Docker environments."
        }
    ],
    "sections": [
        {
            "sectionId": "req-sec-1",
            "startLine": 1,
            "endLine": 7,
            "title": "Core LLM & Multi-Agent Frameworks (LangGraph & LangChain)",
            "code": """# Core LLM & Frameworks
langchain>=0.2.14
langchain-community>=0.2.12
langchain-core>=0.2.33
langchain-openai>=0.1.22
langchain-text-splitters>=0.2.2
langgraph>=0.2.14""",
            "lineByLine": [
                "Line 1: `# Core LLM & Frameworks` - Category comment.",
                "Line 2: `langchain>=0.2.14` - Main LangChain orchestration framework connecting models, prompts, and tools.",
                "Line 3: `langchain-community>=0.2.12` - Community-contributed integrations (like ChromaDB and HuggingFace wrappers).",
                "Line 4: `langchain-core>=0.2.33` - Base abstractions including `Document`, `@tool`, and message schemas.",
                "Line 5: `langchain-openai>=0.1.22` - Integration library for OpenAI GPT models and embeddings.",
                "Line 6: `langchain-text-splitters>=0.2.2` - Text splitters including `RecursiveCharacterTextSplitter` for chunking 10-K filings.",
                "Line 7: `langgraph>=0.2.14` - LangGraph cyclical state machine framework for building stateful multi-agent DAGs."
            ],
            "beginnerConcepts": [
                {
                    "term": "LangGraph (`langgraph`)",
                    "explanation": "The framework used to build our 4-agent graph (`Supervisor -> Quant -> Risk -> Verifier -> END`) with memory checkpointing."
                },
                {
                    "term": "LangChain Core (`langchain-core`)",
                    "explanation": "Provides fundamental building blocks like `Document(page_content, metadata)` and `@tool` decorators."
                }
            ],
            "simpleExplanation": "These packages provide the multi-agent brains of the application, allowing autonomous agents to pass state, call tools, and split text.",
            "whyWrittenThisWay": "Splitting LangChain into modular packages (`core`, `community`, `langgraph`) reduces dependency bloat and keeps execution lightweight.",
            "interviewTips": "Highlight that using LangGraph v0.2+ ensures native support for StateGraph and MemorySaver checkpointing."
        },
        {
            "sectionId": "req-sec-2",
            "startLine": 9,
            "endLine": 16,
            "title": "Data Validation, Vector DB & Hybrid Search (Pydantic, ChromaDB, BM25)",
            "code": """# Data Validation & Typing
pydantic>=2.8.2
pydantic-settings>=2.4.0

# Vector Database & Hybrid Search
chromadb>=0.5.5
rank-bm25>=0.2.2""",
            "lineByLine": [
                "Line 10: `pydantic>=2.8.2` - Pydantic v2 data validation library that enforces strict type safety on `AgentState`.",
                "Line 11: `pydantic-settings>=2.4.0` - Manages environment variables and configuration files (`.env`).",
                "Line 14: `chromadb>=0.5.5` - Local persistent vector database for storing and querying 384-dimensional embeddings.",
                "Line 15: `rank-bm25>=0.2.2` - Lightweight Python implementation of the BM25Okapi keyword ranking algorithm."
            ],
            "beginnerConcepts": [
                {
                    "term": "Pydantic v2",
                    "explanation": "A high-performance Python data validator written in Rust. It guarantees that dictionaries and JSON payloads match their expected types."
                },
                {
                    "term": "ChromaDB & Rank-BM25",
                    "explanation": "The twin search engines of our Hybrid RAG system: ChromaDB handles conceptual meaning, while BM25 handles exact keyword numbers."
                }
            ],
            "simpleExplanation": "Pydantic makes sure data types never get corrupted between agents, ChromaDB stores our vector embeddings, and rank-bm25 searches for exact words and numbers.",
            "whyWrittenThisWay": "Pydantic v2 is 5-10x faster than v1 due to its Rust core, and ChromaDB runs locally without needing an expensive external cloud database.",
            "interviewTips": "Explain: 'I chose Pydantic v2 for sub-millisecond state validation across multi-agent nodes.'"
        },
        {
            "sectionId": "req-sec-3",
            "startLine": 17,
            "endLine": 32,
            "title": "Document Parsing, Evaluation, FastAPI Server & Streamlit UI",
            "code": """# Document Parsing & Financial Data
pypdf>=4.3.1
pymupdf>=1.24.9
pandas>=2.2.2
yfinance>=0.2.41

# Evaluation & Testing (LLM-as-a-Judge)
ragas>=0.1.13
pytest>=8.3.2

# Serving & UI
fastapi>=0.112.1
uvicorn>=0.30.6
streamlit>=1.37.1
python-dotenv>=1.0.1""",
            "lineByLine": [
                "Line 18: `pypdf>=4.3.1` & Line 19: `pymupdf>=1.24.9` - PDF parsing libraries for reading institutional SEC PDF filings.",
                "Line 20: `pandas>=2.2.2` - Tabular data manipulation library for formatting balance sheets and research tables.",
                "Line 21: `yfinance>=0.2.41` - Yahoo Finance market data library for fetching live stock prices and market caps.",
                "Line 24: `ragas>=0.1.13` - Industry-standard evaluation framework for measuring RAG Faithfulness and Groundedness.",
                "Line 25: `pytest>=8.3.2` - Automated unit testing framework for CI/CD regression test suites.",
                "Line 28: `fastapi>=0.112.1` - Fast, modern asynchronous web framework for building REST API microservices.",
                "Line 29: `uvicorn>=0.30.6` - Lightning-fast ASGI web server that runs FastAPI.",
                "Line 30: `streamlit>=1.37.1` - Interactive frontend dashboard framework for equity analysts.",
                "Line 31: `python-dotenv>=1.0.1` - Loads environment variables from `.env` files."
            ],
            "beginnerConcepts": [
                {
                    "term": "FastAPI + Uvicorn",
                    "explanation": "FastAPI is the API code, and Uvicorn is the server engine that handles incoming HTTP requests from users."
                },
                {
                    "term": "Ragas (`ragas`)",
                    "explanation": "The AI evaluation library that calculates our 96.4% Groundedness score."
                },
                {
                    "term": "Streamlit (`streamlit`)",
                    "explanation": "Turns Python scripts into interactive web apps with sliders, buttons, and tables without writing HTML or JavaScript."
                }
            ],
            "simpleExplanation": "These packages handle PDF extraction, live stock quotes, automated Ragas benchmarks, FastAPI REST API serving, and the interactive Streamlit user dashboard.",
            "whyWrittenThisWay": "Combining FastAPI for backend APIs with Streamlit for frontend dashboards gives both technical developers and non-technical analysts the interfaces they need.",
            "interviewTips": "Mention fullstack separation: FastAPI serves programmatic clients, while Streamlit delivers interactive executive dashboards."
        }
    ]
}

# Add both Module 10 items
modules = [m for m in modules if m["id"] not in ["grounding-masterclass", "requirements-guide"]]
modules.append(grounding_module)
modules.append(requirements_module)

output_path = "/Users/narendramishra/GEN AI /code_explanation/src/data/projectData.js"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(f"// MASTER FINAGENT CODE EXPLANATION DATASET\nexport const PROJECT_MODULES = {json.dumps(modules, indent=2)};\n")

print(f"Successfully added requirements.txt to Category 10 in projectData.js! Total modules: {len(modules)}")
