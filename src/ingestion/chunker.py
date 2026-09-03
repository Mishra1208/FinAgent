from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class FinancialChunker:
    """
    Chunks financial documents while preserving financial tabular layouts,
    numerical continuity, and section context.
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Financial-aware separator hierarchy:
        # 1. Major section markers
        # 2. Bullet point line items / tables
        # 3. Double newlines (paragraphs)
        # 4. Single newlines
        # 5. Sentence periods
        # 6. Spaces
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n================================================================================\n",
                "\n\n",
                "\n- ",
                "\n",
                ". ",
                " "
            ]
        )

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Splits a list of section documents into smaller, dense retrieval chunks
        while maintaining inherited metadata and injecting a unique chunk_id.
        """
        chunked_docs = self.splitter.split_documents(documents)
        
        # Enrich each chunk with unique index & token metadata
        for idx, doc in enumerate(chunked_docs):
            doc.metadata["chunk_id"] = f"{doc.metadata.get('ticker', 'CORP')}_{doc.metadata.get('fiscal_year', '2024')}_chunk_{idx}"
            doc.metadata["char_count"] = len(doc.page_content)
            
        return chunked_docs
