import os
import re
from typing import List, Dict, Any
from langchain_core.documents import Document

class SECDocumentLoader:
    """
    Loads and preprocesses SEC Form 10-K and 10-Q filings.
    Extracts structural metadata (Ticker, Fiscal Year, Section Items)
    to enable high-precision filtering during RAG retrieval.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"SEC filing not found at: {file_path}")

    def load(self) -> List[Document]:
        """
        Reads the file and parses major SEC 10-K sections into discrete Document objects.
        """
        with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()

        filename = os.path.basename(self.file_path)
        fn_lower = filename.lower()
        
        # Infer ticker and company
        if "apple" in fn_lower or "aapl" in fn_lower:
            ticker = "AAPL"
            company_name = "Apple Inc."
        elif "morgan_stanley" in fn_lower or "ms_" in fn_lower or fn_lower.startswith("ms"):
            ticker = "MS"
            company_name = "Morgan Stanley"
        elif "microsoft" in fn_lower or "msft" in fn_lower:
            ticker = "MSFT"
            company_name = "Microsoft Corporation"
        else:
            ticker = "CORP"
            company_name = "Enterprise Corporation"

        # Infer year
        year_match = re.search(r"202[0-9]", filename)
        fiscal_year = year_match.group(0) if year_match else "2024"

        # Regex supporting both formatted and raw SEC EDGAR section headers
        section_pattern = r"(?:={10,}\s*\n)?(PART\s+[I|II|III|IV]+[\s\n\-]+ITEM\s+[0-9A-Z\.]+[^\n]*)(?:\n={10,})?"
        
        # Split by sections
        split_positions = [m.start() for m in re.finditer(section_pattern, raw_text, flags=re.IGNORECASE)]
        
        if not split_positions or len(split_positions) < 2:
            # Fallback regex for raw SEC headings
            alt_pattern = r"\n\s*(ITEM\s+[0-9A-Z\.]+\s*[\.\-:]?\s*[A-Z\s,–—]{3,60})\n"
            split_positions = [m.start() for m in re.finditer(alt_pattern, raw_text, flags=re.IGNORECASE)]

        documents = []
        if not split_positions:
            # Single document fallback
            doc = Document(
                page_content=raw_text[:15000],
                metadata={
                    "source": filename,
                    "ticker": ticker,
                    "company": company_name,
                    "fiscal_year": fiscal_year,
                    "section": "PART I - ITEM 1. BUSINESS & RESULTS",
                    "doc_type": "10-K"
                }
            )
            documents.append(doc)
            return documents

        # Add Header document if text precedes first section
        if split_positions[0] > 0:
            header_text = raw_text[:split_positions[0]].strip()
            if header_text:
                documents.append(Document(
                    page_content=header_text[:3000],
                    metadata={
                        "source": filename,
                        "ticker": ticker,
                        "company": company_name,
                        "fiscal_year": fiscal_year,
                        "section": "Header & Overview",
                        "doc_type": "10-K"
                    }
                ))

        # Chunk out each identified section
        for idx in range(len(split_positions)):
            start_pos = split_positions[idx]
            end_pos = split_positions[idx+1] if idx + 1 < len(split_positions) else len(raw_text)
            sec_block = raw_text[start_pos:end_pos].strip()

            lines = sec_block.split("\n")
            first_line = lines[0].replace("=", "").strip()
            sec_title = first_line if len(first_line) > 3 else "SEC 10-K Disclosure"

            doc = Document(
                page_content=sec_block,
                metadata={
                    "source": filename,
                    "ticker": ticker,
                    "company": company_name,
                    "fiscal_year": fiscal_year,
                    "section": sec_title[:60],
                    "doc_type": "10-K"
                }
            )
            documents.append(doc)

        return documents
