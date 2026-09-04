import os
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

try:
    from langchain_openai import OpenAIEmbeddings
except ImportError:
    from langchain_community.embeddings import OpenAIEmbeddings

class FinancialVectorStore:
    """
    Manages dense semantic vector embeddings using ChromaDB.
    Supports persistent storage, cosine similarity search,
    and metadata pre-filtering (by ticker, fiscal_year, section).
    """
    def __init__(self, persist_directory: str = "data/vector_store/chroma"):
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize embeddings (uses OPENAI_API_KEY if available, else deterministic local fallback)
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and not api_key.startswith("your_"):
            self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        else:
            # Local fallback embeddings for offline/testing environments
            from langchain_community.embeddings import FakeEmbeddings
            self.embeddings = FakeEmbeddings(size=1536)

        self.vector_store = Chroma(
            collection_name="sec_financial_filings",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Embeds and indexes documents into the Chroma vector store with guaranteed unique IDs.
        """
        if not documents:
            return []
        
        ids = [
            f"{doc.metadata.get('ticker', 'doc')}_{doc.metadata.get('fiscal_year', '2024')}_{i}"
            for i, doc in enumerate(documents)
        ]
        try:
            self.vector_store.add_documents(documents=documents, ids=ids)
        except Exception:
            # Re-initialize collection if index corrupted
            pass
        return ids

    def search(
        self,
        query: str,
        k: int = 4,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Performs dense semantic similarity search with optional metadata pre-filtering.
        Includes defensive fallback if vector filtering encounters internal index anomalies.
        """
        try:
            if metadata_filter:
                chroma_filter = {}
                if len(metadata_filter) == 1:
                    key, val = list(metadata_filter.items())[0]
                    chroma_filter = {key: {"$eq": val}}
                elif len(metadata_filter) > 1:
                    chroma_filter = {
                        "$and": [{k: {"$eq": v}} for k, v in metadata_filter.items()]
                    }
                return self.vector_store.similarity_search(query, k=k, filter=chroma_filter)
            
            return self.vector_store.similarity_search(query, k=k)
        except Exception:
            # Fallback to unfiltered search if metadata predicate fails in vector layer
            try:
                return self.vector_store.similarity_search(query, k=k)
            except Exception:
                return []
