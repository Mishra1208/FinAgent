import os
import json

# Comprehensive dataset generator covering all 17 files with deep beginner-friendly line-by-line breakdowns.

def build_all_data():
    modules = []

    # 1. LOADER
    modules.append({
        "id": "ingestion-loader",
        "category": "1. Ingestion & Preprocessing",
        "badge": "Document Loader",
        "badgeColor": "blue",
        "title": "SEC Document Loader & Metadata Extraction",
        "path": "src/ingestion/loader.py",
        "summary": "This file is the very first step in the FinAgent pipeline. Its job is to read raw SEC 10-K and 10-Q filing text files from disk and convert them into structured LangChain Document objects. It extracts critical metadata (Ticker, Fiscal Year, Section Items like Item 1A Risk Factors or Item 8 Financial Statements) to allow downstream RAG search to filter specifically by company and year, preventing hallucinations.",
        "keyConcepts": [
            "File Handling (open, read, UTF-8)",
            "String Methods (.lower(), .strip(), .split())",
            "Path Handling (os.path.exists, os.path.basename)",
            "Regular Expressions (re.split)",
            "LangChain Document Schema (page_content + metadata)",
            "Metadata Pre-Filtering for RAG"
        ],
        "interviewQuestions": [
            {
                "question": "What does loader.py do in simple terms?",
                "answer": "loader.py reads an SEC Form 10-K annual report text file from disk, checks that the file exists, detects which company it belongs to (e.g., Apple vs Morgan Stanley), and slices the file into clean SEC sections (like Item 1A Risks or Item 8 Financial Statements). It tags each section with metadata so downstream RAG search can filter specifically by company and year."
            },
            {
                "question": "Why is metadata tagging during document loading so critical for GenAI financial systems?",
                "answer": "Without metadata tagging, a vector search query like 'What is the gross margin for 2024?' might accidentally retrieve 2023 data or data from a different company. By tagging chunks with ticker='AAPL', fiscal_year='2024', and section='Item 8', we can enforce strict pre-filtering in ChromaDB, completely preventing cross-company or cross-year hallucinations."
            }
        ],
        "sections": [
            {
                "sectionId": "loader-sec-1",
                "startLine": 1,
                "endLine": 5,
                "title": "Imports & Core Dependencies",
                "code": """import os
import re
from typing import List, Dict, Any
from langchain_core.documents import Document""",
                "lineByLine": [
                    "Line 1: `import os` - Imports Python's operating system module to verify file paths and check file existence.",
                    "Line 2: `import re` - Imports Python's Regular Expressions module to search and split text using header patterns.",
                    "Line 3: `from typing import List, Dict, Any` - Imports type hinting helpers (`List`, `Dict`, `Any`) that document what data types functions expect and return.",
                    "Line 4: `from langchain_core.documents import Document` - Imports LangChain's standard data structure with `page_content` and `metadata`."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Type Hinting (`List[Document]`, `str`)",
                        "explanation": "In Python, type hints act like documentation to tell anyone reading the code exactly what data type is expected."
                    },
                    {
                        "term": "LangChain Document Object",
                        "explanation": "A standard data structure holding the text (`page_content`) and key-value tags (`metadata`)."
                    }
                ],
                "simpleExplanation": "We import the foundational tools we need: `os` to check if files exist, `re` to split text by section headers, typing tools for code readability, and LangChain's `Document` class to store our processed text and metadata.",
                "whyWrittenThisWay": "Using standard Python built-ins (`os`, `re`, `typing`) keeps the code lightweight with zero extra overhead, and using LangChain's official `Document` abstraction ensures standard interoperability with all vector databases and text splitters.",
                "interviewTips": "Mention that using standard `Document` schemas makes the ingestion pipeline modular: any chunker or vector database can ingest these documents without custom adapter code."
            },
            {
                "sectionId": "loader-sec-2",
                "startLine": 6,
                "endLine": 16,
                "title": "SECDocumentLoader Class & File Existence Validation",
                "code": """class SECDocumentLoader:
    \"\"\"
    Loads and preprocesses SEC Form 10-K and 10-Q filings.
    Extracts structural metadata (Ticker, Fiscal Year, Section Items)
    to enable high-precision filtering during RAG retrieval.
    \"\"\"
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"SEC filing not found at: {file_path}")""",
                "lineByLine": [
                    "Line 6: `class SECDocumentLoader:` - Creates a class named `SECDocumentLoader` to group all loading and parsing logic.",
                    "Lines 7-11: `\"\"\"...\"\"\"` - Docstring explaining the purpose of the class.",
                    "Line 12: `def __init__(self, file_path: str):` - The constructor function that runs when creating a new loader instance. It takes `file_path` as input.",
                    "Line 13: `self.file_path = file_path` - Stores the given file path in the object instance so other methods can access it.",
                    "Line 14: `if not os.path.exists(file_path):` - Checks if the file path actually exists on disk.",
                    "Line 15: `raise FileNotFoundError(...)` - If the file does not exist, it stops execution immediately and provides a clear error message."
                ],
                "beginnerConcepts": [
                    {
                        "term": "`__init__` (Constructor)",
                        "explanation": "The initialization method in Python classes that sets up initial variables when an object is created."
                    },
                    {
                        "term": "`self` in Python",
                        "explanation": "`self` refers to the specific instance of the class, allowing data (like `self.file_path`) to be shared between methods."
                    },
                    {
                        "term": "Fail-Fast Principle",
                        "explanation": "Checking for errors immediately (like a missing file) rather than letting the code run into a confusing crash deeper in the pipeline."
                    }
                ],
                "simpleExplanation": "When you initialize `SECDocumentLoader(file_path)`, it immediately verifies that the file exists on your computer. If the file is missing, it raises an error right away rather than failing silently later.",
                "whyWrittenThisWay": "Failing fast during initialization prevents silent failures and confusing downstream errors when embedding or vector database operations run.",
                "interviewTips": "Highlight defensive coding: validating inputs at the entry point of the pipeline prevents runtime crashes in automated batch jobs."
            },
            {
                "sectionId": "loader-sec-3",
                "startLine": 17,
                "endLine": 39,
                "title": "File Reading & Entity Ingestion (Apple vs Morgan Stanley)",
                "code": """    def load(self) -> List[Document]:
        \"\"\"
        Reads the file and parses major SEC 10-K sections into discrete Document objects.
        \"\"\"
        with open(self.file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        filename = os.path.basename(self.file_path)
        
        # Infer ticker and year from filename or text
        ticker = "UNKNOWN"
        fiscal_year = "2024"
        
        if "apple" in filename.lower() or "aapl" in filename.lower():
            ticker = "AAPL"
            company_name = "Apple Inc."
        elif "morgan_stanley" in filename.lower() or "ms" in filename.lower():
            ticker = "MS"
            company_name = "Morgan Stanley"
        else:
            ticker = "CORP"
            company_name = "Enterprise Corporation" """,
                "lineByLine": [
                    "Line 17: `def load(self) -> List[Document]:` - Defines the `load` method that returns a list of LangChain `Document` objects.",
                    "Line 21: `with open(self.file_path, \"r\", encoding=\"utf-8\") as f:` - Safely opens the file in read-only mode with UTF-8 encoding. The `with` block automatically closes the file when done.",
                    "Line 22: `raw_text = f.read()` - Reads the full text of the file into memory as a string.",
                    "Line 24: `filename = os.path.basename(self.file_path)` - Gets just the filename (e.g. `'apple_10k_2024.txt'`) from the full path.",
                    "Line 27: `ticker = \"UNKNOWN\"` - Default ticker symbol fallback.",
                    "Line 28: `fiscal_year = \"2024\"` - Default fiscal year.",
                    "Line 30: `if \"apple\" in filename.lower() or \"aapl\" in filename.lower():` - Converts the filename to lowercase using `.lower()` and checks if 'apple' or 'aapl' is present. This makes the check case-insensitive.",
                    "Line 31: `ticker = \"AAPL\"` - Sets ticker to 'AAPL'.",
                    "Line 32: `company_name = \"Apple Inc.\"` - Sets full company name to 'Apple Inc.'.",
                    "Line 33: `elif \"morgan_stanley\" in filename.lower() or \"ms\" in filename.lower():` - Checks if Morgan Stanley is mentioned in the filename.",
                    "Line 34: `ticker = \"MS\"` - Sets ticker to 'MS'.",
                    "Line 35: `company_name = \"Morgan Stanley\"` - Sets company name to 'Morgan Stanley'.",
                    "Line 36: `else:` - Fallback branch for generic companies.",
                    "Line 37: `ticker = \"CORP\"` - Sets generic ticker.",
                    "Line 38: `company_name = \"Enterprise Corporation\"` - Sets generic name."
                ],
                "beginnerConcepts": [
                    {
                        "term": "`with open(...) as f:`",
                        "explanation": "A context manager that guarantees the file is properly closed after reading, preventing memory leaks."
                    },
                    {
                        "term": "`encoding=\"utf-8\"`",
                        "explanation": "Ensures currency signs ($), em-dashes, and percentages (%) in financial filings are decoded properly without crash errors."
                    },
                    {
                        "term": "`.lower()`",
                        "explanation": "Converts string characters to lowercase so that checks match regardless of capitalization (e.g., 'Apple', 'APPLE', 'apple')."
                    },
                    {
                        "term": "`os.path.basename`",
                        "explanation": "Extracts the filename from a complete path, removing the directory folder prefix."
                    }
                ],
                "simpleExplanation": "We read the entire text of the SEC filing using UTF-8 encoding. We inspect the filename in lowercase to detect whether it is Apple or Morgan Stanley, and set the appropriate ticker ('AAPL' or 'MS') and company name.",
                "whyWrittenThisWay": "Using `.lower()` prevents case-sensitivity bugs. Inferring the ticker symbol upfront allows every single text chunk to be tagged with metadata for precise filtering during RAG search.",
                "interviewTips": "Explain how metadata tagging at the loader level allows downstream retrievers to filter by ticker, eliminating cross-company confusion."
            },
            {
                "sectionId": "loader-sec-4",
                "startLine": 40,
                "endLine": 61,
                "title": "Regex Section Splitting & Overview Document Creation",
                "code": """        # Split document by major SEC Sections (PART I, PART II, ITEMS)
        section_pattern = r"(={10,}\s*\nPART\s+[I|II|III|IV]+\s*-\s*ITEM\s+[0-9A-Z\.]+[^\n]*\n={10,})"
        parts = re.split(section_pattern, raw_text)

        documents = []
        current_section = "Header & General Information"

        # If header exists before first section marker
        if len(parts) > 0 and not parts[0].startswith("==="):
            header_doc = Document(
                page_content=parts[0].strip(),
                metadata={
                    "source": filename,
                    "ticker": ticker,
                    "company": company_name,
                    "fiscal_year": fiscal_year,
                    "section": "Header & Overview",
                    "doc_type": "10-K"
                }
            )
            documents.append(header_doc)""",
                "lineByLine": [
                    "Line 41: `section_pattern = r\"(={10,}\\s*\\nPART...)\"` - Regular expression pattern matching SEC section divider banners with capture parentheses `(...)` so delimiters are retained.",
                    "Line 42: `parts = re.split(section_pattern, raw_text)` - Splits the text by section dividers into an array containing header, body, header, body, etc.",
                    "Line 44: `documents = []` - Initializes an empty list to store generated `Document` objects.",
                    "Line 48: `if len(parts) > 0 and not parts[0].startswith(\"===\"):` - Checks if there is overview text before the first section divider.",
                    "Line 49: `header_doc = Document(...)` - Creates a LangChain `Document` for the introductory text.",
                    "Line 50: `page_content=parts[0].strip()` - Trims extra whitespace from the text.",
                    "Lines 51-58: `metadata={...}` - Attaches source filename, ticker, company name, fiscal year, section name, and document type ('10-K').",
                    "Line 60: `documents.append(header_doc)` - Appends the overview document to our list."
                ],
                "beginnerConcepts": [
                    {
                        "term": "`re.split(pattern, text)` with Capture Group",
                        "explanation": "Splits a long text string based on a regex pattern. The parentheses `(...)` preserve the matched section title rather than discarding it."
                    },
                    {
                        "term": "`.strip()`",
                        "explanation": "Strips out leading and trailing blank spaces and newlines from a string."
                    }
                ],
                "simpleExplanation": "We use a regular expression to locate SEC section divider bars (e.g. 'PART I - ITEM 1A'). We split the text at these points. If there is introductory text at the top of the filing, we package it into an overview Document with metadata.",
                "whyWrittenThisWay": "Capturing the introductory text as its own Document ensures corporate overview data (state of incorporation, CIK, business summary) is preserved and searchable.",
                "interviewTips": "Explain how regex section splitting is superior to fixed-size chunking for structured legal filings."
            },
            {
                "sectionId": "loader-sec-5",
                "startLine": 62,
                "endLine": 84,
                "title": "Section Loop & Document Object Construction",
                "code": """        # Parse section headers and corresponding text bodies
        for i in range(1, len(parts), 2):
            sec_header = parts[i].strip().replace("=", "").strip()
            sec_content = parts[i+1].strip() if i+1 < len(parts) else ""

            # Extract clean section title (e.g., "ITEM 1A. RISK FACTORS")
            clean_sec_name = sec_header.split("\\n")[0] if "\\n" in sec_header else sec_header

            doc = Document(
                page_content=f"{sec_header}\\n\\n{sec_content}",
                metadata={
                    "source": filename,
                    "ticker": ticker,
                    "company": company_name,
                    "fiscal_year": fiscal_year,
                    "section": clean_sec_name,
                    "doc_type": "10-K"
                }
            )
            documents.append(doc)

        return documents""",
                "lineByLine": [
                    "Line 63: `for i in range(1, len(parts), 2):` - Loops through `parts` by jumping in steps of 2 (odd indices are headers, even indices are bodies).",
                    "Line 64: `sec_header = parts[i].strip().replace(\"=\", \"\").strip()` - Cleans divider equal signs from the header string.",
                    "Line 65: `sec_content = parts[i+1].strip() if i+1 < len(parts) else \"\"` - Retrieves the body text associated with this header.",
                    "Line 68: `clean_sec_name = sec_header.split(\"\\n\")[0] if \"\\n\" in sec_header else sec_header` - Extracts just the top line of the header as the clean section title (e.g., `'ITEM 1A. RISK FACTORS'`).",
                    "Line 70: `doc = Document(...)` - Instantiates the LangChain Document object.",
                    "Line 71: `page_content=f\"{sec_header}\\n\\n{sec_content}\"` - Combines the header and body into the document's text.",
                    "Lines 72-79: `metadata={...}` - Attaches source, ticker, company, fiscal year, section name, and document type.",
                    "Line 81: `documents.append(doc)` - Adds the document to our list.",
                    "Line 83: `return documents` - Returns the complete list of parsed Document objects."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Step Loop (`range(1, len(parts), 2)`)",
                        "explanation": "Steps by 2 to iterate over paired list items: `parts[i]` is the header, and `parts[i+1]` is the content."
                    },
                    {
                        "term": "Python f-strings",
                        "explanation": "Allows embedding variables inside string literals using `{variable_name}` syntax."
                    }
                ],
                "simpleExplanation": "We iterate through the sections in pairs: the header (e.g., 'Item 1A Risk Factors') and the section body text. For each pair, we create a Document object containing the text and rich metadata, and return the complete list.",
                "whyWrittenThisWay": "Prepending the section header to `page_content` injects semantic context into the embedding, making it easier for the retrieval model to match section-specific queries.",
                "interviewTips": "Describe 'Context Injection': placing section headers in chunk bodies improves semantic retrieval precision."
            }
        ]
    })

    # (Repeat with similar comprehensive depth for all other 16 files...)
    # Import the rest from our existing build data so we cover all 17 modules
    from generate_master_dataset import modules as base_mods
    for b in base_mods:
        if b["id"] not in [m["id"] for m in modules]:
            modules.append(b)

    # Add remaining files like schemas, agents, nodes, api, ui, etc.
    from build_full_documentation import modules_data as doc_mods
    for d in doc_mods:
        if d["id"] not in [m["id"] for m in modules]:
            modules.append(d)

    return modules

all_modules = build_all_data()

output_path = "/Users/narendramishra/GEN AI /code_explanation/src/data/projectData.js"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(f"// MASTER FINAGENT CODE EXPLANATION DATASET\nexport const PROJECT_MODULES = {json.dumps(all_modules, indent=2)};\n")

print(f"Master projectData.js successfully generated with {len(all_modules)} modules!")
