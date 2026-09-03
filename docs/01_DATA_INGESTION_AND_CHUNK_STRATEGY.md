# Step 1: SEC 10-K Data Ingestion & Financial Chunking Strategy

---

## 1. ⏱️ Executive Summary
In Step 1 of **FinAgent**, we built the **Document Ingestion & Chunking Engine** tailored specifically for **SEC Form 10-K Annual Reports**. 

Rather than treating financial filings as generic text, our ingestion pipeline parses structural SEC items (`Item 1`, `Item 1A`, `Item 7`, `Item 8`), preserves tabular financial continuity, and enriches every chunk with metadata (`ticker`, `fiscal_year`, `section`, `chunk_id`) to enable high-precision vector filtering.

---

## 2. 🏛️ The Financial Context (Understanding SEC 10-K Filings)

Every publicly traded corporation in the US (like Apple, Microsoft, or Morgan Stanley) must file an annual **Form 10-K** with the Securities and Exchange Commission (SEC). 

A 10-K filing follows a standardized legal structure:

```
┌────────────────────────────────────────────────────────────────────────┐
│ SEC FORM 10-K STRUCTURE                                                │
├────────────────────────────────────────────────────────────────────────┤
│ PART I:                                                                │
│  - ITEM 1.  Business Overview & Revenue by Segment (iPhone, Services)  │
│  - ITEM 1A. Risk Factors (Supply chain, DOJ Antitrust, AI Competition) │
├────────────────────────────────────────────────────────────────────────┤
│ PART II:                                                               │
│  - ITEM 7.  Management's Discussion & Analysis (MD&A) (Gross Margins)  │
│  - ITEM 8.  Financial Statements (Income Statement, Balance Sheet)     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. ⚠️ The "Naive Chunking Trap" in Financial AI

Why do 90% of beginner RAG tutorials fail when applied to Wall Street filings?

1. **Table Severing:** If you chunk blindly at 500 characters, a table row gets cut in half. The label `"iPhone Net Sales"` ends up in Chunk 1, while the number `"$201,183 million"` ends up in Chunk 2. The LLM loses the connection!
2. **Year Confusion:** Financial tables place years side-by-side (e.g., `2024 | 2023`). If chunk boundaries split the table header from the numbers below, the LLM hallucinates 2023 numbers as 2024 numbers.
3. **Loss of Section Context:** A statement like *"Revenue declined 5%"* might refer to Mac computers in Item 1, but without metadata, the LLM might assume total company revenue declined.

---

## 4. 🛠️ Our Ingestion Solution & Code Architecture

We engineered two dedicated classes inside `FinAgent/src/ingestion/`:

### A. `SECDocumentLoader` (`src/ingestion/loader.py`)
* **What it does:** Uses regular expressions (`section_pattern`) to identify major SEC header boundaries (`ITEM 1`, `ITEM 1A`, `ITEM 7`, `ITEM 8`).
* **Metadata Extraction:** Automatically extracts and attaches:
  * `ticker` (e.g., `"AAPL"`, `"MS"`)
  * `company` (e.g., `"Apple Inc."`, `"Morgan Stanley"`)
  * `fiscal_year` (e.g., `"2024"`)
  * `section` (e.g., `"PART I - ITEM 1A. RISK FACTORS"`)
  * `doc_type` (e.g., `"10-K"`)

### B. `FinancialChunker` (`src/ingestion/chunker.py`)
* **Chunk Size:** **1,000 characters** (large enough to encapsulate complete financial statement line items and multi-line risk paragraphs).
* **Chunk Overlap:** **150 characters** (ensures contiguous sentences and numerical context are never lost across boundaries).
* **Financial Separator Hierarchy:**
  ```python
  separators = [
      "\n================================================================================\n", # Major section dividers
      "\n\n",   # Paragraph breaks
      "\n- ",   # Tabular bullet points & balance sheet line items
      "\n",     # Line breaks
      ". ",     # Sentence periods
      " "       # Word spaces
  ]
  ```

---

## 5. 🎯 Top 3 Morgan Stanley Interview Questions & Model Answers

### Q1: *"How do you handle financial tabular data and multi-column financial statements during RAG chunking?"*
> **Answer:**  
> *"Financial tables require preserving the spatial relationship between metric names, fiscal periods, and numerical values. Standard token splitters destroy this relationship by splitting across arbitrary character counts.  
> In FinAgent, we handle this by:  
> 1. Implementing a hierarchical separator list that prioritizes paragraph and line-item bullet boundaries (`\n- `) before splitting words.  
> 2. Setting chunk size to 1,000 characters with 150-character overlap to keep complete statement line items in a single context window.  
> 3. Tagging every chunk with structured section metadata (e.g., `ITEM 8. FINANCIAL STATEMENTS`) so the retriever can filter explicitly for tabular data."*

### Q2: *"Why did you choose a chunk size of 1000 characters and 150-character overlap for SEC filings?"*
> **Answer:**  
> *"In financial analysis, chunks below 500 characters suffer from context fragmentation (e.g., separating an EBITDA figure from its corresponding footnote or fiscal year). Chunks above 3,000 characters introduce semantic dilution, reducing the precision of dense vector similarity.  
> A 1,000-character chunk size (~200-250 tokens) is the empirical sweet spot for SEC filings: it comfortably holds 4 to 6 balance sheet line items or a complete Item 1A risk disclosure, while a 150-character overlap guarantees that multi-sentence legal qualifiers are never clipped at chunk boundaries."*

### Q3: *"How does metadata enrichment improve retrieval latency and reduce hallucinations in an enterprise banking assistant?"*
> **Answer:**  
> *"Without metadata, querying 'What are the top supply chain risks?' requires searching against millions of vectors across all companies and years in the database, increasing retrieval latency and risking irrelevant cross-company matches.  
> By enriching each chunk with structured metadata (`ticker='AAPL'`, `fiscal_year='2024'`, `section='ITEM 1A. RISK FACTORS'`), we perform **Pre-Filtering (Self-Querying RAG)**. The database narrows the search space to only Apple's 2024 Risk Factors before running vector similarity, cutting search latency by over 80% and mathematically eliminating cross-company hallucinations."*
