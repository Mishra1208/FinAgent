import os
import json

def generate_all_modules():
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
                    "Line 1: `import os` - Imports Python's built-in operating system module to interact with file paths and verify file existence on your computer.",
                    "Line 2: `import re` - Imports Python's built-in Regular Expressions module, which allows searching and splitting text based on complex patterns (like finding SEC headers).",
                    "Line 3: `from typing import List, Dict, Any` - Imports type hinting helpers (`List`, `Dict`, `Any`) that document what data types functions expect and return.",
                    "Line 4: `from langchain_core.documents import Document` - Imports LangChain's standard data structure. A `Document` has two key parts: `page_content` (the actual text) and `metadata` (a dictionary storing info like source, ticker, section, etc.)."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Type Hinting (`List[Document]`, `str`)",
                        "explanation": "In Python, type hints don't change how code runs, but they act like documentation to tell anyone reading the code exactly what data type is expected."
                    },
                    {
                        "term": "LangChain Document Object",
                        "explanation": "Think of a LangChain Document like an index card: on the front is the text (`page_content`), and on the back is the label/sticker (`metadata` with ticker, year, and page number)."
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

    # 2. CHUNKER
    modules.append({
        "id": "ingestion-chunker",
        "category": "1. Ingestion & Preprocessing",
        "badge": "Chunker",
        "badgeColor": "blue",
        "title": "Financial Chunker & Table Structure Preservation",
        "path": "src/ingestion/chunker.py",
        "summary": "Splits SEC section documents into dense, context-preserving chunks optimized for financial retrieval. Configured with a 1,000-character chunk size and 150-character overlap using custom hierarchical separators designed specifically to prevent breaking financial tables, numerical statements, or bullet points in half.",
        "keyConcepts": [
            "RecursiveCharacterTextSplitter",
            "Chunk Size (1,000 chars) & Chunk Overlap (150 chars)",
            "Hierarchical Separators for Financial Tables",
            "Deterministic Chunk ID Generation",
            "Metadata Inheritance"
        ],
        "interviewQuestions": [
            {
                "question": "Why did you choose a chunk size of 1000 characters with 150 characters overlap?",
                "answer": "In SEC 10-K filings, paragraphs and financial tables typically span between 600 to 900 characters. A chunk size of 1,000 characters ensures that an entire financial table or risk disclosure item fits into a single embedding chunk without fragmentation. The 150-character (~30 token) overlap prevents critical boundary figures or trailing footnotes from being lost between adjacent chunks."
            },
            {
                "question": "What happens if a financial table is split across two chunks in naive chunking?",
                "answer": "In naive chunking, table headers (e.g., 'In Millions', 'Year Ended Sept 2024') get separated from the actual numerical rows. The LLM then hallucinates the units or fiscal years. Our custom separator hierarchy splits at major section headers and double newlines first, keeping tables intact."
            }
        ],
        "sections": [
            {
                "sectionId": "chunker-sec-1",
                "startLine": 1,
                "endLine": 4,
                "title": "Imports & Splitter Modules",
                "code": """from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter""",
                "lineByLine": [
                    "Line 1: `from langchain_core.documents import Document` - Imports LangChain's Document class.",
                    "Line 2: `from langchain_text_splitters import RecursiveCharacterTextSplitter` - Imports LangChain's intelligent text splitter that splits text hierarchically based on a list of separator characters."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Recursive Text Splitting",
                        "explanation": "Unlike simple splitters that chop text at fixed character counts, a recursive splitter tries to split by paragraph first, then newline, then space, keeping sentences and paragraphs together."
                    }
                ],
                "simpleExplanation": "We import LangChain's `RecursiveCharacterTextSplitter`, which splits documents into smaller pieces while trying to keep paragraphs and sentences whole.",
                "whyWrittenThisWay": "`RecursiveCharacterTextSplitter` is the standard for RAG applications because it preserves document structure better than naive character slicing.",
                "interviewTips": "Highlight that recursive chunking respects document structure far better than fixed token window slicing."
            },
            {
                "sectionId": "chunker-sec-2",
                "startLine": 5,
                "endLine": 27,
                "title": "FinancialChunker Initialization & Separator Hierarchy",
                "code": """class FinancialChunker:
    \"\"\"
    Chunks financial documents while preserving financial tabular layouts,
    numerical continuity, and section context.
    \"\"\"

    def __init__(self, chunk_size=1000, chunk_overlap=150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\\n================================================================================\\n",
                "\\n\\n",
                "\\n- ",
                "\\n",
                ". ",
                " "
            ]
        )""",
                "lineByLine": [
                    "Line 5: `class FinancialChunker:` - Defines the chunker class for financial filings.",
                    "Line 11: `def __init__(self, chunk_size=1000, chunk_overlap=150):` - Constructor setting default `chunk_size=1000` characters and `chunk_overlap=150` characters.",
                    "Line 12: `self.chunk_size = chunk_size` - Stores chunk size setting.",
                    "Line 13: `self.chunk_overlap = chunk_overlap` - Stores overlap setting.",
                    "Line 15: `self.splitter = RecursiveCharacterTextSplitter(...)` - Initializes the splitter with custom separators.",
                    "Lines 19-24: `separators=[...]` - Priority order of split points: 1) SEC major divider bar, 2) Double newlines (paragraphs), 3) Bullet points (`\\n- `), 4) Single newlines (table rows), 5) Sentences (`. `), 6) Words (` `)."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Chunk Size",
                        "explanation": "The maximum number of characters each chunk should contain (1,000 characters is ~200-250 words)."
                    },
                    {
                        "term": "Chunk Overlap",
                        "explanation": "The number of characters shared between neighboring chunks (150 chars). This ensures context at the boundary is not lost."
                    },
                    {
                        "term": "Separator Hierarchy",
                        "explanation": "The priority order of characters where the splitter is allowed to cut. It tries to cut at double newlines before resorting to cutting mid-sentence."
                    }
                ],
                "simpleExplanation": "We set up our chunker with a 1,000 character target size and a 150 character overlap. We specify custom separators so it cuts at section dividers and paragraph breaks first, keeping financial tables and lists intact.",
                "whyWrittenThisWay": "Custom separator hierarchy prevents cutting tables in half and solves the orphan row problem where numbers appear without their metric labels.",
                "interviewTips": "Explain why custom separators are necessary for financial tables: preserving line breaks prevents columns and numbers from getting jumbled."
            },
            {
                "sectionId": "chunker-sec-3",
                "startLine": 28,
                "endLine": 41,
                "title": "chunk_documents & Unique Chunk ID Injection",
                "code": """    def chunk_documents(self, documents):
        \"\"\"
        Splits a list of section documents into smaller, dense retrieval chunks
        while maintaining inherited metadata and injecting a unique chunk_id.
        \"\"\"
        chunked_docs = self.splitter.split_documents(documents)

        for idx, doc in enumerate(chunked_docs):
            doc.metadata[
                "chunk_id"] = f"{doc.metadata.get('ticker', 'CORP')}_{doc.metadata.get('fiscal_year', '2024')}_chunk_{idx}"
            doc.metadata["char_count"] = len(doc.page_content)

        return chunked_docs""",
                "lineByLine": [
                    "Line 28: `def chunk_documents(self, documents):` - Method taking a list of Document objects and splitting them into smaller chunks.",
                    "Line 33: `chunked_docs = self.splitter.split_documents(documents)` - Executes the recursive text split on all input documents.",
                    "Line 35: `for idx, doc in enumerate(chunked_docs):` - Loops through each chunk with an index counter `idx`.",
                    "Lines 36-37: `doc.metadata[\"chunk_id\"] = f\"{ticker}_{fiscal_year}_chunk_{idx}\"` - Generates and attaches a unique, deterministic ID (e.g., `'AAPL_2024_chunk_14'`) into the chunk's metadata.",
                    "Line 38: `doc.metadata[\"char_count\"] = len(doc.page_content)` - Records the exact character length of the chunk.",
                    "Line 40: `return chunked_docs` - Returns the final list of metadata-enriched chunks."
                ],
                "beginnerConcepts": [
                    {
                        "term": "`enumerate(list)`",
                        "explanation": "A Python loop helper that gives you both the item index (`idx` = 0, 1, 2...) and the item (`doc`) simultaneously."
                    },
                    {
                        "term": "Deterministic Chunk ID",
                        "explanation": "A predictable unique name given to every chunk (like `AAPL_2024_chunk_0`) that allows tracking and citing exact source documents."
                    }
                ],
                "simpleExplanation": "We split all documents into chunks. Then we loop through every chunk and give it a unique ID (like `AAPL_2024_chunk_5`) and record its character count in its metadata.",
                "whyWrittenThisWay": "Having unique, deterministic chunk IDs is essential for deduplication, citation tracking in research memos, and computing Reciprocal Rank Fusion (RRF) scores in Hybrid RAG.",
                "interviewTips": "Explain that unique chunk IDs allow the Citation Verifier Agent to audit exact claims back to the source chunk."
            }
        ]
    })

    # 3. VECTOR STORE (ChromaDB)
    modules.append({
        "id": "rag-vector-store",
        "category": "2. Hybrid RAG Layer",
        "badge": "Vector DB",
        "badgeColor": "indigo",
        "title": "Vector Store & Dense Semantic Embeddings (ChromaDB)",
        "path": "src/rag/vector_store.py",
        "summary": "Implements the dense semantic vector search layer using ChromaDB and HuggingFace SentenceTransformer embeddings (all-MiniLM-L6-v2). Converts financial text chunks into 384-dimensional mathematical vectors, persists them to disk, and executes cosine similarity searches with metadata pre-filtering.",
        "keyConcepts": [
            "Dense Vector Embeddings (all-MiniLM-L6-v2)",
            "ChromaDB Persistent Vector Store",
            "Cosine Similarity Search",
            "Metadata Pre-Filtering (`filter={'ticker': 'AAPL'}`)",
            "Embedding Dimensions (384-d)"
        ],
        "interviewQuestions": [
            {
                "question": "What is a vector embedding and how does ChromaDB use it?",
                "answer": "An embedding model converts text into a mathematical list of numbers (a vector). Chunks with similar semantic meaning (e.g. 'supply chain disruption' and 'manufacturing delays') end up close together in geometric vector space. ChromaDB computes cosine distance between the user query vector and all chunk vectors to retrieve the most conceptually relevant chunks."
            },
            {
                "question": "Why did you use all-MiniLM-L6-v2 instead of OpenAI text-embedding-ada-002?",
                "answer": "all-MiniLM-L6-v2 produces compact 384-dimensional embeddings that run locally on CPU with ultra-low latency (~15ms) and zero API subscription costs. For local offline demoing and CI/CD pipelines, it delivers exceptional performance without external API rate limit risks."
            }
        ],
        "sections": [
            {
                "sectionId": "vstore-sec-1",
                "startLine": 1,
                "endLine": 18,
                "title": "Imports & Vector Store Initializer",
                "code": """import os
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class FinancialVectorStore:
    \"\"\"
    Dense Semantic Vector Store using ChromaDB and HuggingFace Embeddings.
    Handles embedding computation, persistent storage, and dense similarity search.
    \"\"\"
    def __init__(self, persist_directory: str = "data/vector_store/chroma"):
        self.persist_directory = persist_directory
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
        self.vector_store: Optional[Chroma] = None""",
                "lineByLine": [
                    "Line 1: `import os` - Python OS module for file path operations.",
                    "Line 2: `from typing import List, Dict, Any, Optional` - Type annotations (`Optional` means a variable can be a value or `None`).",
                    "Line 3: `from langchain_core.documents import Document` - LangChain's Document schema.",
                    "Line 4: `from langchain_community.vectorstores import Chroma` - ChromaDB vector database wrapper.",
                    "Line 5: `from langchain_community.embeddings import HuggingFaceEmbeddings` - HuggingFace local embedding model runner.",
                    "Line 7: `class FinancialVectorStore:` - The class encapsulating ChromaDB operations.",
                    "Line 12: `def __init__(self, persist_directory: str = \"data/vector_store/chroma\"):` - Constructor taking the storage folder path.",
                    "Line 13: `self.persist_directory = persist_directory` - Stores the directory path on disk.",
                    "Lines 14-17: `self.embedding_model = HuggingFaceEmbeddings(...)` - Loads the `all-MiniLM-L6-v2` neural network model to run on CPU.",
                    "Line 18: `self.vector_store: Optional[Chroma] = None` - Initializes the vector store reference to None until documents are ingested."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Vector Database (ChromaDB)",
                        "explanation": "A specialized database designed to store and quickly search high-dimensional numerical vectors (embeddings)."
                    },
                    {
                        "term": "all-MiniLM-L6-v2 Embedding Model",
                        "explanation": "A lightweight transformer AI model that translates English sentences into 384 numbers that represent their underlying meaning."
                    },
                    {
                        "term": "`device: cpu`",
                        "explanation": "Specifies that the model should run on the computer's standard CPU processor without requiring an expensive NVIDIA GPU."
                    }
                ],
                "simpleExplanation": "We initialize the `FinancialVectorStore` class by setting a folder path on disk where vectors will be saved, and loading the `all-MiniLM-L6-v2` embedding model to run on the CPU.",
                "whyWrittenThisWay": "Encapsulating ChromaDB in a dedicated class allows swapping vector databases (e.g. to Qdrant or Pinecone) in the future without changing any agent code.",
                "interviewTips": "State that abstracting database operations behind a class follows the Repository Design Pattern."
            },
            {
                "sectionId": "vstore-sec-2",
                "startLine": 19,
                "endLine": 45,
                "title": "add_documents Method & Vector Persistence",
                "code": """    def add_documents(self, documents: List[Document]):
        \"\"\"
        Ingests document chunks into ChromaDB with embeddings and metadata.
        \"\"\"
        if not documents:
            return

        os.makedirs(self.persist_directory, exist_ok=True)
        if self.vector_store is None:
            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embedding_model,
                persist_directory=self.persist_directory
            )
        else:
            self.vector_store.add_documents(documents)""",
                "lineByLine": [
                    "Line 19: `def add_documents(self, documents: List[Document]):` - Ingestion method that takes a list of document chunks.",
                    "Line 23: `if not documents:` - If the input list is empty, exit early to avoid wasted compute.",
                    "Line 26: `os.makedirs(self.persist_directory, exist_ok=True)` - Creates the directory on disk if it doesn't already exist (`exist_ok=True` prevents errors if it already exists).",
                    "Line 27: `if self.vector_store is None:` - Checks if this is the first time documents are added.",
                    "Lines 28-32: `self.vector_store = Chroma.from_documents(...)` - Calculates embeddings for all chunks and writes the vector index to disk.",
                    "Lines 33-34: `else: self.vector_store.add_documents(documents)` - If the database is already running, appends the new chunks to the existing index."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Vector Persistence",
                        "explanation": "Saving computed vectors to the hard drive so you don't have to re-compute expensive AI embeddings every time the server restarts."
                    },
                    {
                        "term": "`os.makedirs(..., exist_ok=True)`",
                        "explanation": "Creates a folder directory tree. If the directory already exists, it does nothing rather than throwing a folder already exists error."
                    }
                ],
                "simpleExplanation": "When we pass document chunks into `add_documents()`, it ensures the save folder exists, computes 384-dimensional embeddings for each chunk, and saves the vectors to disk in ChromaDB.",
                "whyWrittenThisWay": "Persisting to disk avoids re-embedding 150-page files on every query, dramatically reducing startup time and compute costs.",
                "interviewTips": "Explain: 'Vector persistence in ChromaDB avoids re-embedding overhead on cold restarts.'"
            },
            {
                "sectionId": "vstore-sec-3",
                "startLine": 46,
                "endLine": 73,
                "title": "search Method & Metadata Pre-Filtering",
                "code": """    def search(
        self,
        query: str,
        k: int = 4,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        \"\"\"
        Executes semantic similarity search with optional metadata pre-filtering.
        \"\"\"
        if self.vector_store is None:
            return []

        search_kwargs = {"k": k}
        if metadata_filter:
            search_kwargs["filter"] = metadata_filter

        results = self.vector_store.similarity_search(query, **search_kwargs)
        return results""",
                "lineByLine": [
                    "Line 46: `def search(self, query: str, k: int = 4, metadata_filter = None):` - Searches the vector store for the `k` most relevant chunks matching the user's text query.",
                    "Line 54: `if self.vector_store is None: return []` - Safety guard returning an empty list if no documents have been indexed.",
                    "Line 56: `search_kwargs = {\"k\": k}` - Creates a dictionary of search options with the number of chunks to return (`k=4`).",
                    "Line 57: `if metadata_filter:` - If a filter was provided (e.g. `{'ticker': 'AAPL'}`).",
                    "Line 58: `search_kwargs[\"filter\"] = metadata_filter` - Adds the filter to search options so ChromaDB pre-filters candidates before scoring.",
                    "Line 60: `results = self.vector_store.similarity_search(query, **search_kwargs)` - Converts the query to a vector embedding, performs cosine similarity search, and returns top matches.",
                    "Line 61: `return results` - Returns the list of top matching `Document` chunks."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Cosine Similarity",
                        "explanation": "A math formula measuring the cosine of the angle between two vectors. If the angle is 0 (cosine = 1.0), the meanings are identical."
                    },
                    {
                        "term": "Metadata Pre-Filtering (`filter`)",
                        "explanation": "Telling the database: 'Only search inside Apple chunks and ignore everything else' before ranking."
                    },
                    {
                        "term": "`**search_kwargs` (Dictionary Unpacking)",
                        "explanation": "A Python shortcut to unpack key-value pairs from a dictionary into named function arguments."
                    }
                ],
                "simpleExplanation": "When a user asks a question, this method turns the question into a vector embedding, applies any metadata filter (e.g. only AAPL files), and uses cosine similarity to find and return the top `k` most similar document chunks.",
                "whyWrittenThisWay": "Using metadata pre-filtering eliminates cross-company false positives before similarity calculations happen, drastically improving accuracy.",
                "interviewTips": "Emphasize the difference between pre-filtering (filtering before vector search) and post-filtering (filtering results after search, which risks returning 0 matches)."
            }
        ]
    })

    # 4. BM25 RETRIEVER
    modules.append({
        "id": "rag-bm25-retriever",
        "category": "2. Hybrid RAG Layer",
        "badge": "BM25 Search",
        "badgeColor": "indigo",
        "title": "BM25 Sparse Keyword Retriever",
        "path": "src/rag/bm25_retriever.py",
        "summary": "Implements sparse lexical keyword search using the BM25 (Best Matching 25) probabilistic algorithm with custom financial term tokenization. Ensures exact matching for numbers, tickers, ratios, and formal SEC Item titles where semantic embedding models often miss exact alphanumeric strings.",
        "keyConcepts": [
            "BM25Okapi Algorithm",
            "Term Frequency (TF) & Inverse Document Frequency (IDF)",
            "Financial Tokenization (Preserving $, %, .)",
            "Sparse Keyword Search",
            "Exact Match Scoring"
        ],
        "interviewQuestions": [
            {
                "question": "What is BM25 and why is it essential for financial documents?",
                "answer": "BM25 is a ranking algorithm based on exact word frequencies (Term Frequency) and rarity across documents (Inverse Document Frequency). While embedding models understand concepts like 'business risks', they often fail to distinguish '$391,035M' from '$383,285M' or 'Item 1A' from 'Item 1'. BM25 finds exact alphanumeric matches with 100% confidence."
            }
        ],
        "sections": [
            {
                "sectionId": "bm25-sec-1",
                "startLine": 1,
                "endLine": 13,
                "title": "Imports & BM25 Class Definition",
                "code": """import re
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

class FinancialBM25Retriever:
    \"\"\"
    Sparse Lexical Retriever using the BM25Okapi ranking algorithm.
    Excels at exact keyword matching for financial metrics, tickers, and table headers.
    \"\"\"
    def __init__(self):
        self.bm25: Optional[BM25Okapi] = None
        self.documents: List[Document] = []
        self.corpus_tokens: List[List[str]] = []""",
                "lineByLine": [
                    "Line 1: `import re` - Python regular expression module for custom word splitting.",
                    "Line 4: `from rank_bm25 import BM25Okapi` - Imports the Okapi BM25 ranking algorithm from the `rank_bm25` library.",
                    "Line 6: `class FinancialBM25Retriever:` - The class managing the BM25 keyword index.",
                    "Line 11: `self.bm25: Optional[BM25Okapi] = None` - Stores the compiled BM25 index.",
                    "Line 12: `self.documents: List[Document] = []` - Stores the original document chunks.",
                    "Line 13: `self.corpus_tokens: List[List[str]] = []` - Stores the tokenized words of all documents."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Sparse Retrieval (BM25)",
                        "explanation": "A search technique that matches exact words in a text index, similar to a Google search for exact phrases."
                    },
                    {
                        "term": "Inverted Index / Corpus Tokens",
                        "explanation": "A breakdown of every word that appears in each document, allowing near-instant lookups."
                    }
                ],
                "simpleExplanation": "We set up the `FinancialBM25Retriever` class with variables to hold our document chunks and their tokenized word lists.",
                "whyWrittenThisWay": "Storing the original `Document` objects alongside the BM25 index allows returning full LangChain `Document` objects with metadata intact.",
                "interviewTips": "State that BM25 requires no neural network inference or GPU, making it exceptionally fast (sub-millisecond)."
            },
            {
                "sectionId": "bm25-sec-2",
                "startLine": 14,
                "endLine": 35,
                "title": "Financial Tokenization & Indexing",
                "code": """    def tokenize(self, text: str) -> List[str]:
        \"\"\"
        Tokenizes financial text while preserving alphanumeric tokens,
        percentages, dollar figures, and item identifiers.
        \"\"\"
        # Convert to lower and split on non-alphanumeric chars (preserving %, $, .)
        tokens = re.findall(r"\\b[A-Za-z0-9\\$\\.%\\-]+\\b", text.lower())
        return tokens

    def index_documents(self, documents: List[Document]):
        \"\"\"
        Indexes a collection of Document chunks into the BM25 inverted index.
        \"\"\"
        if not documents:
            return
        self.documents = documents
        self.corpus_tokens = [self.tokenize(doc.page_content) for doc in documents]
        self.bm25 = BM25Okapi(self.corpus_tokens)""",
                "lineByLine": [
                    "Line 14: `def tokenize(self, text: str) -> List[str]:` - Custom tokenizer method.",
                    "Line 20: `tokens = re.findall(r\"\\b[A-Za-z0-9\\$\\.%\\-]+\\b\", text.lower())` - Splits text into words while explicitly keeping `$`, `%`, `.`, and `-` so numbers like `$391,035` or `46.2%` stay intact as unified tokens.",
                    "Line 21: `return tokens` - Returns list of cleaned words/symbols.",
                    "Line 23: `def index_documents(self, documents: List[Document]):` - Builds the BM25 search index from a list of chunks.",
                    "Line 29: `self.corpus_tokens = [self.tokenize(doc.page_content) for doc in documents]` - Tokenizes every chunk in the dataset.",
                    "Line 30: `self.bm25 = BM25Okapi(self.corpus_tokens)` - Compiles the Okapi BM25 statistical index."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Tokenization",
                        "explanation": "The process of breaking a continuous paragraph of text into individual words or symbols (tokens)."
                    },
                    {
                        "term": "Financial Symbol Preservation",
                        "explanation": "Standard tokenizers throw away '$' and '%'. Our custom regex preserves '$100' and '46.2%' as whole tokens so exact financial figures match properly."
                    }
                ],
                "simpleExplanation": "We break down every document chunk into words, keeping numbers, dollar signs, and percentage signs intact, and compile a BM25 keyword index.",
                "whyWrittenThisWay": "Preserving currency symbols and decimals is crucial in finance so that searching for '$391,035M' matches '$391,035M' exactly rather than generic numbers.",
                "interviewTips": "Highlight domain-specific tokenization: preserving financial punctuation prevents data corruption in numerical queries."
            },
            {
                "sectionId": "bm25-sec-3",
                "startLine": 36,
                "endLine": 72,
                "title": "BM25 Search & Metadata Filtering",
                "code": """    def search(
        self,
        query: str,
        k: int = 4,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        \"\"\"
        Executes BM25 keyword search with optional metadata filtering.
        \"\"\"
        if self.bm25 is None or not self.documents:
            return []

        tokenized_query = self.tokenize(query)
        if not tokenized_query:
            return []

        # Get raw BM25 scores across all corpus documents
        scores = self.bm25.get_scores(tokenized_query)

        # Pair scores with documents and apply metadata filter if provided
        scored_docs = []
        for idx, score in enumerate(scores):
            doc = self.documents[idx]
            if metadata_filter:
                match = all(doc.metadata.get(key) == val for key, val in metadata_filter.items())
                if not match:
                    continue
            scored_docs.append((score, doc))

        # Sort descending by BM25 score
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:k]]""",
                "lineByLine": [
                    "Line 36: `def search(self, query, k=4, metadata_filter=None):` - Executes BM25 search.",
                    "Line 48: `tokenized_query = self.tokenize(query)` - Tokenizes the user's search query.",
                    "Line 53: `scores = self.bm25.get_scores(tokenized_query)` - Calculates BM25 keyword relevance scores across all chunks.",
                    "Line 57: `for idx, score in enumerate(scores):` - Loops through every document score.",
                    "Line 60: `match = all(doc.metadata.get(key) == val ...)` - Verifies metadata filter (e.g. ticker == 'AAPL').",
                    "Line 62: `if not match: continue` - Skips documents that belong to other companies.",
                    "Line 63: `scored_docs.append((score, doc))` - Stores the score and document pair.",
                    "Line 66: `scored_docs.sort(key=lambda x: x[0], reverse=True)` - Sorts the results highest score first.",
                    "Line 67: `return [doc for score, doc in scored_docs[:k]]` - Returns the top `k` matching document chunks."
                ],
                "beginnerConcepts": [
                    {
                        "term": "BM25 Score",
                        "explanation": "A positive numerical score showing how frequently the search terms appear in a chunk, normalized by chunk length."
                    },
                    {
                        "term": "`lambda x: x[0]`",
                        "explanation": "A quick anonymous Python function that tells the `.sort()` method to sort by the first item in the tuple (the numerical score)."
                    }
                ],
                "simpleExplanation": "We tokenize the user query, compute BM25 keyword matching scores for every chunk, filter out any documents that don't match our metadata requirements (e.g. wrong company), and return the top `k` chunks with the highest scores.",
                "whyWrittenThisWay": "Filtering during scoring guarantees that non-matching documents are discarded before selecting the top results.",
                "interviewTips": "Explain why BM25 scores are unbounded positive numbers, which is why rank-based fusion (RRF) is needed to combine them with cosine similarity scores."
            }
        ]
    })

    # 5. HYBRID RETRIEVER (RRF)
    modules.append({
        "id": "rag-hybrid-retriever",
        "category": "2. Hybrid RAG Layer",
        "badge": "Hybrid RAG",
        "badgeColor": "indigo",
        "title": "Hybrid Retriever & Reciprocal Rank Fusion (RRF)",
        "path": "src/rag/hybrid_retriever.py",
        "summary": "Combines Dense Semantic Vector Search (ChromaDB) and Sparse Lexical Keyword Search (BM25) using the Reciprocal Rank Fusion (RRF) algorithm. Queries both retrievers in parallel, scores candidates by their rank positions, and re-ranks documents to achieve peak retrieval accuracy across both conceptual and numerical queries.",
        "keyConcepts": [
            "Hybrid RAG Architecture",
            "Reciprocal Rank Fusion (RRF)",
            "RRF Formula: sum(1 / (60 + rank))",
            "Dense + Sparse Candidate Pooling",
            "Scale-Invariant Re-ranking"
        ],
        "interviewQuestions": [
            {
                "question": "What is Reciprocal Rank Fusion (RRF) and why is it better than linear score addition?",
                "answer": "Dense cosine similarity scores (scaled between -1 and 1) and sparse BM25 scores (unbounded positive floats) have completely different statistical distributions. Linearly adding them requires fragile alpha/beta weighting that breaks on different query types. RRF is scale-invariant: it ranks documents purely based on their rank positions in each list using the formula RRF(d) = sum(1 / (60 + rank))."
            }
        ],
        "sections": [
            {
                "sectionId": "rrf-sec-1",
                "startLine": 1,
                "endLine": 23,
                "title": "Imports & Hybrid Retriever Initialization",
                "code": """from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from src.rag.vector_store import FinancialVectorStore
from src.rag.bm25_retriever import FinancialBM25Retriever

class FinancialHybridRetriever:
    \"\"\"
    Hybrid Retriever combining Dense Vector Search (ChromaDB)
    and Sparse Keyword Search (BM25) using Reciprocal Rank Fusion (RRF).
    
    Ensures that both conceptual semantics (e.g., 'supply chain vulnerabilities')
    and exact keyword numbers/tickers (e.g., 'AAPL', '46.2%') achieve peak retrieval accuracy.
    \"\"\"
    def __init__(
        self,
        vector_store: FinancialVectorStore,
        bm25_retriever: FinancialBM25Retriever,
        rrf_k: int = 60
    ):
        self.vector_store = vector_store
        self.bm25_retriever = bm25_retriever
        self.rrf_k = rrf_k  # Smoothing constant for Reciprocal Rank Fusion""",
                "lineByLine": [
                    "Line 1: `from typing import ...` - Type annotations.",
                    "Line 3: `from src.rag.vector_store import FinancialVectorStore` - Imports dense vector store.",
                    "Line 4: `from src.rag.bm25_retriever import FinancialBM25Retriever` - Imports sparse BM25 retriever.",
                    "Line 6: `class FinancialHybridRetriever:` - The hybrid retriever combining both engines.",
                    "Line 18: `self.vector_store = vector_store` - Reference to ChromaDB store.",
                    "Line 19: `self.bm25_retriever = bm25_retriever` - Reference to BM25 index.",
                    "Line 20: `self.rrf_k = rrf_k` - Smoothing constant (default 60) for Reciprocal Rank Fusion."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Hybrid RAG",
                        "explanation": "Using two different search methods (semantic meaning + exact word matching) together to get the best of both worlds."
                    },
                    {
                        "term": "RRF Constant (k = 60)",
                        "explanation": "A standard smoothing number proven by information retrieval research that balances top results without letting single outliers dominate."
                    }
                ],
                "simpleExplanation": "We initialize the `FinancialHybridRetriever` by giving it both our dense vector store (ChromaDB) and our sparse keyword retriever (BM25), along with the standard RRF constant of 60.",
                "whyWrittenThisWay": "Injecting both retrievers into the constructor follows dependency injection, making the hybrid retriever easy to unit-test and maintain.",
                "interviewTips": "Mention dependency injection: passing retriever instances in `__init__` enables clean mocking during testing."
            },
            {
                "sectionId": "rrf-sec-2",
                "startLine": 24,
                "endLine": 38,
                "title": "Parallel Candidate Fetching (2x Over-fetch)",
                "code": """    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        \"\"\"
        Executes parallel dense and sparse searches, then fuses and re-ranks
        candidates using the Reciprocal Rank Fusion (RRF) algorithm.
        \"\"\"
        # 1. Fetch top candidates from both retrievers (fetch 2x top_k to ensure rich fusion candidate pool)
        fetch_k = top_k * 2
        dense_results = self.vector_store.search(query, k=fetch_k, metadata_filter=metadata_filter)
        sparse_results = self.bm25_retriever.search(query, k=fetch_k, metadata_filter=metadata_filter)""",
                "lineByLine": [
                    "Line 24: `def retrieve(self, query, top_k=4, metadata_filter=None):` - Main retrieval method.",
                    "Line 35: `fetch_k = top_k * 2` - Doubles the number of candidates to fetch (e.g. 2 * 4 = 8 candidates).",
                    "Line 36: `dense_results = self.vector_store.search(...)` - Queries ChromaDB for top 8 dense semantic matches.",
                    "Line 37: `sparse_results = self.bm25_retriever.search(...)` - Queries BM25 for top 8 keyword matches."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Candidate Pool (Over-fetching)",
                        "explanation": "Fetching 8 candidates instead of 4 from each search engine so that when we fuse them together, we have a richer set of options to find the true best matches."
                    }
                ],
                "simpleExplanation": "We ask both search engines (ChromaDB and BM25) to return their top 8 candidate chunks so we have plenty of candidates to compare and re-rank.",
                "whyWrittenThisWay": "Over-fetching candidates ensures that a chunk that ranked #5 in dense search but #1 in keyword search isn't left behind.",
                "interviewTips": "Explain: 'Over-fetching 2x candidates guarantees high recall before rank fusion narrows down to top_k.'"
            },
            {
                "sectionId": "rrf-sec-3",
                "startLine": 39,
                "endLine": 68,
                "title": "Reciprocal Rank Fusion Algorithm & Re-ranking",
                "code": """        # 2. Calculate Reciprocal Rank Fusion (RRF) Scores
        # Formula: RRF_Score(d) = sum( 1 / (60 + rank_i(d)) )
        doc_scores: Dict[str, float] = {}
        doc_map: Dict[str, Document] = {}

        # Score Dense Results
        for rank, doc in enumerate(dense_results):
            doc_id = doc.metadata.get("chunk_id", doc.page_content[:50])
            doc_map[doc_id] = doc
            doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))

        # Score Sparse (BM25) Results
        for rank, doc in enumerate(sparse_results):
            doc_id = doc.metadata.get("chunk_id", doc.page_content[:50])
            doc_map[doc_id] = doc
            doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))

        # 3. Sort by fused RRF score descending
        sorted_doc_ids = sorted(doc_scores.keys(), key=lambda did: doc_scores[did], reverse=True)

        # 4. Attach fused RRF score into metadata and return top_k
        fused_documents: List[Document] = []
        for did in sorted_doc_ids[:top_k]:
            doc = doc_map[did]
            # Copy doc and inject retrieval score
            doc.metadata["rrf_score"] = round(doc_scores[did], 6)
            fused_documents.append(doc)

        return fused_documents""",
                "lineByLine": [
                    "Line 40: `# Formula: RRF_Score(d) = sum( 1 / (60 + rank_i(d)) )` - The mathematical formula.",
                    "Line 41: `doc_scores = {}` - Dictionary storing each document's cumulative RRF score.",
                    "Line 42: `doc_map = {}` - Dictionary mapping chunk ID to the Document object.",
                    "Line 45: `for rank, doc in enumerate(dense_results):` - Loops through dense results by rank (0, 1, 2...).",
                    "Line 48: `doc_scores[doc_id] += 1.0 / (60 + rank + 1)` - Adds `1 / (60 + rank + 1)` to the document's score.",
                    "Line 51: `for rank, doc in enumerate(sparse_results):` - Loops through BM25 results by rank.",
                    "Line 54: `doc_scores[doc_id] += 1.0 / (60 + rank + 1)` - Adds BM25 rank score to the same document.",
                    "Line 57: `sorted_doc_ids = sorted(..., key=lambda did: doc_scores[did], reverse=True)` - Sorts documents by highest fused score.",
                    "Lines 61-66: `for did in sorted_doc_ids[:top_k]: ...` - Injects `rrf_score` into document metadata and returns the top `k` chunks."
                ],
                "beginnerConcepts": [
                    {
                        "term": "Reciprocal Rank Scoring",
                        "explanation": "If a document is rank 0, its score is 1/(60+1) = 0.01639. If it appears in both lists at rank 0, its score is doubled to 0.03278, pushing it to the very top."
                    },
                    {
                        "term": "Score Normalization Problem",
                        "explanation": "Cosine similarity is between -1 and 1, while BM25 is between 0 and 50. You cannot simply add them. RRF fixes this by using rank position instead of raw scores."
                    }
                ],
                "simpleExplanation": "We iterate through the candidates from both search engines. For each document, we add `1 / (60 + rank + 1)` to its score. Any document that scored well in both search engines gets the highest total score, and we return the top `k` best documents.",
                "whyWrittenThisWay": "RRF is scale-invariant and requires no manual score weighting, making it robust across queries of all types.",
                "interviewTips": "Walk through an RRF example in the interview to prove your deep understanding of information retrieval math."
            }
        ]
    })

    # (Add all other files: tools, schemas, guardrails, graph, nodes, evaluation, api, ui, infra, tests)
    # Let's import all remaining modules similarly...
    return modules

print("Generating full dataset...")
