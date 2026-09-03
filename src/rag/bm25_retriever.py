import re
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

class FinancialBM25Retriever:
    """
    Sparse keyword retriever based on the BM25Okapi algorithm.
    Excels at exact term matching for tickers (AAPL, MS),
    specific fiscal years (2024, 2023), and exact financial metrics (EBITDA, ROTCE, Gross Margin).
    """
    def __init__(self):
        self.documents: List[Document] = []
        self.corpus_tokens: List[List[str]] = []
        self.bm25: Optional[BM25Okapi] = None

    def _tokenize(self, text: str) -> List[str]:
        """
        Cleans and tokenizes text, preserving financial numbers, percentages, and acronyms.
        """
        # Split on whitespace and punctuation, keeping alphanumeric terms and key markers
        tokens = re.findall(r"\b[A-Za-z0-9\$\%\.\-]+\b", text.lower())
        return tokens

    def index_documents(self, documents: List[Document]):
        """
        Builds the BM25 index over the provided document chunks.
        """
        self.documents = documents
        self.corpus_tokens = [self._tokenize(doc.page_content) for doc in documents]
        if self.corpus_tokens:
            self.bm25 = BM25Okapi(self.corpus_tokens)

    def search(
        self,
        query: str,
        k: int = 4,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Performs BM25 keyword search, scoring chunks and applying metadata pre-filtering.
        """
        if not self.bm25 or not self.documents:
            return []

        tokenized_query = self._tokenize(query)
        if not tokenized_query:
            return []

        scores = self.bm25.get_scores(tokenized_query)
        
        # Pair documents with their BM25 scores
        scored_docs = list(zip(self.documents, scores))
        
        # Apply metadata filtering if specified
        if metadata_filter:
            filtered_scored = []
            for doc, score in scored_docs:
                matches_all = True
                for key, val in metadata_filter.items():
                    if doc.metadata.get(key) != val:
                        matches_all = False
                        break
                if matches_all:
                    filtered_scored.append((doc, score))
            scored_docs = filtered_scored

        # Sort descending by BM25 score
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k documents
        return [doc for doc, score in scored_docs[:k]]
