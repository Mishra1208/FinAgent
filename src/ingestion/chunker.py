from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class FinancialChunker:
    """
    Chunks financial documents while preserving financial tabular layouts,
    numerical continuity, and section context.
    """

    def __init__(self, chunk_size=1000, chunk_overlap=150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

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

    def chunk_documents(self, documents):
        """
        Splits a list of section documents into smaller, dense retrieval chunks
        while maintaining inherited metadata and injecting a unique chunk_id.
        """
        chunked_docs = self.splitter.split_documents(documents)

        for idx, doc in enumerate(chunked_docs):
            doc.metadata[
                "chunk_id"] = f"{doc.metadata.get('ticker', 'CORP')}_{doc.metadata.get('fiscal_year', '2024')}_chunk_{idx}"
            doc.metadata["char_count"] = len(doc.page_content)

        return chunked_docs
