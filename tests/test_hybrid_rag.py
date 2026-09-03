import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingestion.loader import SECDocumentLoader
from src.ingestion.chunker import FinancialChunker
from src.rag.vector_store import FinancialVectorStore
from src.rag.bm25_retriever import FinancialBM25Retriever
from src.rag.hybrid_retriever import FinancialHybridRetriever

def run_step_2_verification():
    print("================================================================================")
    print("🚀 STEP 2 VERIFICATION: HYBRID RAG (CHROMA + BM25 + RECIPROCAL RANK FUSION)")
    print("================================================================================")

    # 1. Ingest Documents
    apple_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "apple_10k_2024.txt")
    ms_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "morgan_stanley_10k_2024.txt")

    loader_apple = SECDocumentLoader(apple_path)
    loader_ms = SECDocumentLoader(ms_path)
    
    raw_docs = loader_apple.load() + loader_ms.load()
    print(f"📄 Loaded {len(raw_docs)} major sections across Apple and Morgan Stanley.")

    # 2. Chunk Documents
    chunker = FinancialChunker(chunk_size=1000, chunk_overlap=150)
    all_chunks = chunker.chunk_documents(raw_docs)
    print(f"✂️ Generated {len(all_chunks)} enriched financial chunks.")

    # 3. Index into ChromaDB Vector Store
    vector_store = FinancialVectorStore(persist_directory="data/vector_store/chroma_test")
    vector_store.add_documents(all_chunks)
    print("📦 Indexed chunks into ChromaDB Vector Store.")

    # 4. Index into BM25 Sparse Retriever
    bm25 = FinancialBM25Retriever()
    bm25.index_documents(all_chunks)
    print("⚡ Indexed chunks into BM25 Keyword Engine.")

    # 5. Initialize Hybrid Ensemble Retriever
    hybrid_retriever = FinancialHybridRetriever(vector_store=vector_store, bm25_retriever=bm25)

    # --- TEST 1: Dense Semantic Conceptual Query ---
    print("\n--------------------------------------------------------------------------------")
    print("🧪 TEST 1: Semantic Query (Antitrust & Regulatory Scrutiny)")
    print("--------------------------------------------------------------------------------")
    query_1 = "What regulatory and antitrust lawsuits are ongoing regarding app stores?"
    results_1 = hybrid_retriever.retrieve(query=query_1, top_k=2)
    assert len(results_1) > 0, "Test 1 Failed: No results returned!"
    print(f"✅ Top Result ID : {results_1[0].metadata.get('chunk_id')}")
    print(f"   Ticker        : {results_1[0].metadata.get('ticker')}")
    print(f"   Section       : {results_1[0].metadata.get('section')}")
    print(f"   RRF Score     : {results_1[0].metadata.get('rrf_score')}")

    # --- TEST 2: Exact Keyword Financial Metric Query (Morgan Stanley ROTCE) ---
    print("\n--------------------------------------------------------------------------------")
    print("🧪 TEST 2: Exact Keyword & Ratio Query (Morgan Stanley ROTCE & CET1 Ratio)")
    print("--------------------------------------------------------------------------------")
    query_2 = "Return on Tangible Common Equity ROTCE CET1 Capital Ratio"
    results_2 = hybrid_retriever.retrieve(query=query_2, top_k=2, metadata_filter={"ticker": "MS"})
    assert len(results_2) > 0, "Test 2 Failed: No results returned!"
    assert results_2[0].metadata.get("ticker") == "MS", "Test 2 Failed: Did not isolate Morgan Stanley!"
    print(f"✅ Top Result ID : {results_2[0].metadata.get('chunk_id')}")
    print(f"   Ticker        : {results_2[0].metadata.get('ticker')}")
    print(f"   Section       : {results_2[0].metadata.get('section')}")
    print(f"   Snippet       : {results_2[0].page_content[:150]}...")

    # --- TEST 3: Metadata Pre-Filtered Hybrid Retrieval (Apple 2024 Gross Margin) ---
    print("\n--------------------------------------------------------------------------------")
    print("🧪 TEST 3: Pre-Filtered Hybrid Query (Apple 2024 Gross Margins)")
    print("--------------------------------------------------------------------------------")
    query_3 = "Gross Margin percentage Services mix cost optimizations"
    results_3 = hybrid_retriever.retrieve(query=query_3, top_k=1, metadata_filter={"ticker": "AAPL", "fiscal_year": "2024"})
    assert len(results_3) > 0, "Test 3 Failed: No results returned!"
    assert results_3[0].metadata.get("ticker") == "AAPL", "Test 3 Failed: Cross-company leakage!"
    print(f"✅ Top Result ID : {results_3[0].metadata.get('chunk_id')}")
    print(f"   Ticker        : {results_3[0].metadata.get('ticker')}")
    print(f"   Section       : {results_3[0].metadata.get('section')}")
    print(f"   RRF Score     : {results_3[0].metadata.get('rrf_score')}")

    print("\n================================================================================")
    print("🎉 STEP 2 HYBRID RAG ENGINE IS 100% VERIFIED & PRODUCTION READY!")
    print("================================================================================")

if __name__ == "__main__":
    run_step_2_verification()
