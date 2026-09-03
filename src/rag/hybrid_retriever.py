from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from src.rag.vector_store import FinancialVectorStore
from src.rag.bm25_retriever import FinancialBM25Retriever

class FinancialHybridRetriever:
    """
    Hybrid Retriever combining Dense Vector Search (ChromaDB)
    and Sparse Keyword Search (BM25) using Reciprocal Rank Fusion (RRF).
    
    Ensures that both conceptual semantics (e.g., 'supply chain vulnerabilities')
    and exact keyword numbers/tickers (e.g., 'AAPL', '46.2%') achieve peak retrieval accuracy.
    """
    def __init__(
        self,
        vector_store: FinancialVectorStore,
        bm25_retriever: FinancialBM25Retriever,
        rrf_k: int = 60
    ):
        self.vector_store = vector_store
        self.bm25_retriever = bm25_retriever
        self.rrf_k = rrf_k  # Smoothing constant for Reciprocal Rank Fusion

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Executes parallel dense and sparse searches, then fuses and re-ranks
        candidates using the Reciprocal Rank Fusion (RRF) algorithm.
        """
        # 1. Fetch top candidates from both retrievers (fetch 2x top_k to ensure rich fusion candidate pool)
        fetch_k = top_k * 2
        dense_results = self.vector_store.search(query, k=fetch_k, metadata_filter=metadata_filter)
        sparse_results = self.bm25_retriever.search(query, k=fetch_k, metadata_filter=metadata_filter)

        # 2. Calculate Reciprocal Rank Fusion (RRF) Scores
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

        return fused_documents
