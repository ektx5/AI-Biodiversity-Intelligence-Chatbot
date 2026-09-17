from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_FAISS_PATH = 'vectorstore/db_faiss'

class RAGPipeline:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})
        self.db = FAISS.load_local(DB_FAISS_PATH, self.embeddings, allow_dangerous_deserialization=True)

    def retrieve_context(self, query, k=3):
        docs = self.db.similarity_search(query, k=k)
        context = '
'.join([doc.page_content for doc in docs])
        return context
