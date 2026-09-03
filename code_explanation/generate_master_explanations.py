import os
import json

BASE_DIR = "/Users/narendramishra/GEN AI /code_explanation/FinAgent"

# We will construct in-depth, beginner-friendly, line-by-line breakdowns for every file.
# Every section will have:
# - lineByLine: list of line-by-line simple explanations
# - beginnerConcepts: list of { term, explanation }
# - simpleExplanation: rich narrative breakdown
# - whyWrittenThisWay: in-depth design rationale & alternatives
# - interviewTips: interview talking points and gotchas

modules_data = [
    # =========================================================================
    # 1. INGESTION & PREPROCESSING: src/ingestion/loader.py
    # =========================================================================
    {
        "id": "ingestion-loader",
        "category": "1. Ingestion & Preprocessing",
        "badge": "Document Loader",
        "badgeColor": "blue",
        "title": "SEC Document Loader & Metadata Extraction",
        "path": "src/ingestion/loader.py",
        "summary": "This file is the very first step in the FinAgent pipeline. Its job is to read raw SEC 10-K and 10-Q filing text files from your disk and transform them into structured 'Document' objects. Instead of treating a 150-page filing as one big block of text, this loader identifies the company (Apple vs Morgan Stanley), detects the fiscal year (2024), and uses regular expression patterns to split the filing into clean sections (like Item 1A Risk Factors or Item 8 Financial Statements).",
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
                "answer": "loader.py is responsible for taking a raw text file of an SEC annual report (Form 10-K), checking that the file actually exists, determining which company it belongs to (e.g., Apple or Morgan Stanley), and slicing the file into distinct SEC sections (like Item 1A Risks or Item 8 Balance Sheets). It tags each section with metadata so downstream RAG search can filter specifically by company and year."
            },
            {
                "question": "Why is metadata tagging during document loading so critical for GenAI financial systems?",
                "answer": "Without metadata tagging, a vector search query like 'What is the gross margin for 2024?' might accidentally retrieve 2023 data or even data from a different company. By tagging chunks with ticker='AAPL', fiscal_year='2024', and section='Item 8', we can enforce strict pre-filtering in ChromaDB, completely preventing cross-company or cross-year hallucinations."
            }
        ],
        "sections": [
            {
                "sectionId": "loader-sec-1",
                "startLine": 1,
                "endLine": 5,
                "title": "Imports & Essential Dependencies",
                "code": """import os
import re
from typing import List, Dict, Any
from langchain_core.documents import Document""",
                "lineByLine": [
                    "Line 1: `import os` - Imports Python's built-in operating system module to interact with file paths and verify file existence on your computer.",
                    "Line 2: `import re` - Imports Python's built-in Regular Expressions module, which allows searching and splitting text based on complex patterns (like finding SEC headers).",
                    "Line 3: `from typing import List, Dict, Any` - Imports type hinting helpers. `List` means a collection of items, `Dict` means key-value pairs (like JSON), and `Any` means a value that could be any data type. This helps developers and IDEs understand what data types functions expect and return.",
                    "Line 4: `from langchain_core.documents import Document` - Imports LangChain's standard data structure. A `Document` has two key parts: `page_content` (the actual text) and `metadata` (a dictionary storing info like source, ticker, section, etc.)."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Type Hinting (`List[Document]`, `str`)",
                        "explanation": "In Python, type hints don't change how code runs, but they act like documentation to tell anyone reading the code exactly what data type is expected (e.g., a string or a list of Document objects)."
                    },
                    {
                        "term": "LangChain Document Object",
                        "explanation": "Think of a LangChain Document like an index card: on the front is the text (`page_content`), and on the back is the label/sticker (`metadata` with ticker, year, and page number)."
                    }
                ],
                "simpleExplanation": "We import the foundational tools we need: `os` to check if the file exists on the computer, `re` to split text by section headers, typing tools to keep our code clean and typed, and LangChain's `Document` class to hold our processed text and metadata.",
                "whyWrittenThisWay": "We use standard Python built-ins (`os`, `re`, `typing`) so there is zero extra overhead, and we use LangChain's official `Document` abstraction so our loaded documents plug directly into any standard chunker, retriever, or vector store.",
                "interviewTips": "Mention that using standard `Document` schemas makes the ingestion pipeline modular: any chunker or vector database can ingest these documents without custom adapter code."
            },
            {
                "sectionId": "loader-sec-2",
                "startLine": 6,
                "endLine": 16,
                "title": "SECDocumentLoader Class & Path Validation",
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
                    "Line 6: `class SECDocumentLoader:` - Creates a new blueprint/class called `SECDocumentLoader` to group all loading logic together.",
                    "Lines 7-11: `\"\"\"...\"\"\"` - A Python docstring that explains what this class does for other engineers.",
                    "Line 12: `def __init__(self, file_path: str):` - The constructor function that runs automatically whenever you create a new instance (e.g., `loader = SECDocumentLoader('path/to/file.txt')`). It takes `file_path` as an input.",
                    "Line 13: `self.file_path = file_path` - Stores the given file path inside the object (`self`) so other methods in the class can use it.",
                    "Line 14: `if not os.path.exists(file_path):` - Checks if the file actually exists on the hard drive. `os.path.exists` returns `True` if found, `False` if missing.",
                    "Line 15: `raise FileNotFoundError(f\"SEC filing not found at: {file_path}\")` - If the file does not exist, it immediately stops the program with an error message indicating the exact missing file path."
                ],
                "beginnerConcepts": [
                    {
                        "term": "`__init__` (Constructor)",
                        "explanation": "Special initialization function in Python classes. When you create an object from a class, `__init__` is the first thing that runs to set up initial variables."
                    },
                    {
                        "term": "`self` in Python",
                        "explanation": "`self` represents the specific instance of the class. It allows variables (like `self.file_path`) to be remembered and shared across different functions inside that class."
                    },
                    {
                        "term": "`raise FileNotFoundError(...)` (Fail-Fast)",
                        "explanation": "Instead of letting the code proceed with an empty or broken file and crashing confusingly later, 'raising an error' immediately alerts the developer with a clear, helpful message."
                    }
                ],
                "simpleExplanation": "This sets up the loader class. When you give it a file path, it immediately checks if the file exists on your computer. If the file is missing, it raises an error right away rather than failing silently later.",
                "whyWrittenThisWay": "This follows the 'Fail-Fast' principle. If a file path is mistyped or missing, throwing an explicit `FileNotFoundError` right at the start saves hours of debugging down the pipeline.",
                "interviewTips": "Interviewers love defensive programming: explain that validating file existence in `__init__` ensures downstream database and embedding operations never attempt to process null inputs."
            },
            {
                "sectionId": "loader-sec-3",
                "startLine": 17,
                "endLine": 39,
                "title": "Reading File & Automatic Entity Detection (Apple vs Morgan Stanley)",
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
                    "Line 17: `def load(self) -> List[Document]:` - Defines the main method `load()` which takes no extra arguments and promises to return a list of LangChain `Document` objects.",
                    "Line 21: `with open(self.file_path, \"r\", encoding=\"utf-8\") as f:` - Safely opens the file in read-only mode (`\"r\"`) using UTF-8 encoding. The `with` statement guarantees that the file is automatically closed when done, even if an error occurs.",
                    "Line 22: `raw_text = f.read()` - Reads the entire text content of the file into a variable named `raw_text`.",
                    "Line 24: `filename = os.path.basename(self.file_path)` - Extracts just the file name (e.g., `'apple_10k_2024.txt'`) from the full path (e.g., `'/Users/user/data/apple_10k_2024.txt'`).",
                    "Line 27: `ticker = \"UNKNOWN\"` - Sets default fallback ticker if no company matches.",
                    "Line 28: `fiscal_year = \"2024\"` - Sets default fiscal year to 2024.",
                    "Line 30: `if \"apple\" in filename.lower() or \"aapl\" in filename.lower():` - Checks if 'apple' or 'aapl' is present in the filename. `.lower()` turns uppercase letters to lowercase so `'Apple_10k'` or `'AAPL'` are both matched.",
                    "Line 31: `ticker = \"AAPL\"` - Sets ticker symbol to 'AAPL'.",
                    "Line 32: `company_name = \"Apple Inc.\"` - Sets full legal name to 'Apple Inc.'.",
                    "Line 33: `elif \"morgan_stanley\" in filename.lower() or \"ms\" in filename.lower():` - If not Apple, checks if 'morgan_stanley' or 'ms' is in the filename.",
                    "Line 34: `ticker = \"MS\"` - Sets ticker to 'MS'.",
                    "Line 35: `company_name = \"Morgan Stanley\"` - Sets company name to 'Morgan Stanley'.",
                    "Line 36: `else:` - Fallback if the file belongs to another company.",
                    "Line 37: `ticker = \"CORP\"` - Sets generic ticker.",
                    "Line 38: `company_name = \"Enterprise Corporation\"` - Sets generic corporate name."
                ],
                "beginnerConcepts": [
                    {
                        "term": "`with open(...) as f:` (Context Manager)",
                        "explanation": "In Python, opening a file locks computer resources. Using `with` ensures Python automatically closes the file the moment reading finishes, preventing memory leaks and locked files."
                    },
                    {
                        "term": "`encoding=\"utf-8\"`",
                        "explanation": "Financial documents contain special symbols like '$', '%', '—' (em-dashes), and quotes. Specifying `utf-8` prevents character corruption and crash errors."
                    },
                    {
                        "term": "`os.path.basename(path)`",
                        "explanation": "Extracts just the end filename (e.g. `'apple_10k_2024.txt'`) from a long directory path (`'/Users/john/project/data/raw/apple_10k_2024.txt'`)."
                    },
                    {
                        "term": "`.lower()`",
                        "explanation": "Converts all letters in a string to lowercase. Why? If a user names a file `'APPLE_10K.txt'` or `'apple_10k.txt'`, `.lower()` turns both into `'apple_10k.txt'` so our `if` check works 100% of the time without failing on uppercase letters."
                    }
                ],
                "simpleExplanation": "We open the file and read all its text into memory using UTF-8 so special financial symbols don't get corrupted. Then, we look at the filename to identify which company it is (e.g. Apple vs Morgan Stanley) so we can attach the company's ticker symbol ('AAPL' or 'MS') to every piece of text we extract.",
                "whyWrittenThisWay": "Using `.lower()` prevents case-sensitivity bugs. Inferring ticker and company name from the filename creates automatic entity tagging, which is what allows the vector database to filter queries specifically by company.",
                "interviewTips": "Explain: 'I used case-insensitive filename inference combined with metadata tagging to ensure multi-company files in the same directory are automatically segregated without hardcoding.'"
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
                    "Line 40: `# Split document by major SEC Sections...` - Comment describing the logic.",
                    "Line 41: `section_pattern = r\"(={10,}\\s*\\nPART\\s+[I|II|III|IV]+\\s*-\\s*ITEM\\s+[0-9A-Z\\.]+[^\n]*\\n={10,})\"` - Regular expression pattern that matches SEC header dividers (e.g., `==========\\nPART I - ITEM 1A. RISK FACTORS\\n==========`). The parenthesis `(...)` capture the header so `re.split` keeps the header text.",
                    "Line 42: `parts = re.split(section_pattern, raw_text)` - Splits the entire raw text into an array containing the header, the body, the next header, the next body, etc.",
                    "Line 44: `documents = []` - Creates an empty list to collect all created `Document` objects.",
                    "Line 45: `current_section = \"Header & General Information\"` - Default section title for the intro text.",
                    "Line 48: `if len(parts) > 0 and not parts[0].startswith(\"===\"):` - Checks if there is introductory text at the very top of the filing before the first formal section divider.",
                    "Line 49: `header_doc = Document(...)` - Creates a LangChain `Document` object for this overview text.",
                    "Line 50: `page_content=parts[0].strip()` - The text content of the header, with extra leading/trailing whitespace removed via `.strip()`.",
                    "Lines 51-58: `metadata={...}` - Attaches source filename, ticker, company name, fiscal year, section name, and document type ('10-K') as metadata.",
                    "Line 60: `documents.append(header_doc)` - Adds this overview document to our document collection list."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Regular Expressions (`re.split` with Capture Group)",
                        "explanation": "Standard string `.split()` throws away the delimiter. By putting parentheses `(...)` in our regex pattern, `re.split` splits the text but keeps the section title so we can use it as the section name."
                    },
                    {
                        "term": "`.strip()`",
                        "explanation": "Removes unnecessary blank spaces, tabs, and newlines from the start and end of a text string, keeping data clean."
                    },
                    {
                        "term": "`documents.append(item)`",
                        "explanation": "Adds a new item to the end of a Python list."
                    }
                ],
                "simpleExplanation": "We use a regex pattern to find where each major SEC section begins (e.g. 'PART I - ITEM 1A'). We split the 150-page document into individual sections. If there is introductory text at the very top before the first section, we package it into a Document object with metadata and save it.",
                "whyWrittenThisWay": "SEC Form 10-K filings have a strict legal layout. By splitting on section boundaries rather than arbitrary 500-word blocks, we preserve section integrity (e.g., Risk Factors stay together, Balance Sheets stay together).",
                "interviewTips": "Interview talking point: 'I chose structural section splitting over naive token-window splitting because financial questions are section-specific (e.g., risk queries belong in Item 1A, financial ratios in Item 8).'"
            },
            {
                "sectionId": "loader-sec-5",
                "startLine": 62,
                "endLine": 84,
                "title": "Looping Over Sections & Constructing Metadata-Enriched Documents",
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
                    "Line 63: `for i in range(1, len(parts), 2):` - Loops through the `parts` array starting at index 1 and stepping by 2. Why step by 2? Because odd indices (1, 3, 5) hold the section headers, and even indices (2, 4, 6) hold the corresponding section text bodies!",
                    "Line 64: `sec_header = parts[i].strip().replace(\"=\", \"\").strip()` - Cleans the header string by removing equal sign divider characters (`==========`) and trimming whitespace.",
                    "Line 65: `sec_content = parts[i+1].strip() if i+1 < len(parts) else \"\"` - Gets the text body following that header, safely handling the end of the list.",
                    "Line 68: `clean_sec_name = sec_header.split(\"\\n\")[0] if \"\\n\" in sec_header else sec_header` - Extracts just the first line of the header (e.g., `'PART I - ITEM 1A. RISK FACTORS'`) to use as a clean section name in metadata.",
                    "Line 70: `doc = Document(...)` - Instantiates the LangChain `Document` object.",
                    "Line 71: `page_content=f\"{sec_header}\\n\\n{sec_content}\"` - Combines the section title and the body content together as the document text.",
                    "Lines 72-79: `metadata={...}` - Attaches source filename, ticker, company name, fiscal year, clean section name, and document type ('10-K').",
                    "Line 81: `documents.append(doc)` - Adds this section document to our list.",
                    "Line 83: `return documents` - Returns the full list of parsed `Document` objects ready for chunking and embedding."
                ],
                "beginnerConcepts": [
                    {
                        "term": "`range(1, len(parts), 2)` (Step Loop)",
                        "explanation": "`range(start, stop, step)` creates a sequence of numbers. Stepping by 2 lets us jump directly to each header index (1, 3, 5, 7) and grab its partner text body at (i+1)."
                    },
                    {
                        "term": "f-strings (`f\"{sec_header}\\n\\n{sec_content}\"` )",
                        "explanation": "Formatted strings in Python. Putting `f` in front of quotes lets you embed variables inside `{}` directly into the text."
                    },
                    {
                        "term": "`.replace(\"=\", \"\")`",
                        "explanation": "Finds all '=' divider characters and replaces them with nothing, cleaning away formatting clutter."
                    }
                ],
                "simpleExplanation": "We loop through all sections in pairs: the section header (e.g., 'Item 1A Risk Factors') and the text that follows it. For each section, we create a LangChain `Document` with the text and rich metadata (ticker, company, year, section title), and return the complete list.",
                "whyWrittenThisWay": "Prepending the section header to `page_content` ensures the embedding model understands what section the text belongs to, which boosts retrieval accuracy when users search for specific items.",
                "interviewTips": "Highlight 'Context Enrichment': including the section title directly inside the page text gives embedding models stronger semantic context for retrieval."
            }
        ]
    }
]
print("Building master generator...")
