from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_FAISS_PATH = PROJECT_ROOT / 'vectorstore' / 'db_faiss'

class RAGPipeline:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})
        if not DB_FAISS_PATH.exists():
            raise FileNotFoundError(
                f'Knowledge base not found at {DB_FAISS_PATH}. '
                'Run "python src/knowledge_base.py" first.'
            )
        self.db = FAISS.load_local(str(DB_FAISS_PATH), self.embeddings, allow_dangerous_deserialization=True)

    def retrieve_context(self, query, k=3):
        docs = self.db.similarity_search(query, k=k)
        return '\n\n'.join(
            f"Source: {Path(doc.metadata.get('source', 'unknown')).name}\n{doc.page_content}"
            for doc in docs
        )
