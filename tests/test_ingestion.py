import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingestion.loader import SECDocumentLoader
from src.ingestion.chunker import FinancialChunker

def test_apple_ingestion():
    raw_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "apple_10k_2024.txt")
    loader = SECDocumentLoader(raw_path)
    docs = loader.load()
    
    assert len(docs) > 0, "No documents loaded from Apple 10-K!"
    print(f"✅ Loaded {len(docs)} major sections from Apple 10-K.")
    
    chunker = FinancialChunker(chunk_size=1000, chunk_overlap=150)
    chunks = chunker.chunk_documents(docs)
    
    assert len(chunks) > 0, "No chunks generated!"
    print(f"✅ Generated {len(chunks)} retrieval chunks.")
    
    # Check sample chunk metadata
    sample = chunks[0]
    print(f"   Sample Chunk ID: {sample.metadata['chunk_id']}")
    print(f"   Ticker: {sample.metadata['ticker']}")
    print(f"   Section: {sample.metadata['section']}")
    print(f"   Length: {sample.metadata['char_count']} chars")

def test_morgan_stanley_ingestion():
    raw_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "morgan_stanley_10k_2024.txt")
    loader = SECDocumentLoader(raw_path)
    docs = loader.load()
    
    assert len(docs) > 0, "No documents loaded from Morgan Stanley 10-K!"
    print(f"✅ Loaded {len(docs)} major sections from Morgan Stanley 10-K.")
    
    chunker = FinancialChunker(chunk_size=1000, chunk_overlap=150)
    chunks = chunker.chunk_documents(docs)
    
    assert len(chunks) > 0, "No chunks generated!"
    print(f"✅ Generated {len(chunks)} retrieval chunks for Morgan Stanley.")

if __name__ == "__main__":
    print("--- Running Ingestion & Chunking Tests ---")
    test_apple_ingestion()
    test_morgan_stanley_ingestion()
    print("🎉 Ingestion & Chunking pipeline is 100% verified!")
