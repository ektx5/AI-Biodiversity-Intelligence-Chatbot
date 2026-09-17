from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_FAISS_PATH = PROJECT_ROOT / 'vectorstore' / 'db_faiss'
DATA_PATH = PROJECT_ROOT / 'data'

def create_vector_db():
    print('Loading documents...')
    loader = DirectoryLoader(str(DATA_PATH), glob='*.txt', loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    documents = loader.load()
    if not documents:
        raise ValueError(f'No .txt knowledge documents found in {DATA_PATH}')
    print(f'Loaded {len(documents)} documents.')

    print('Splitting text...')
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    print('Creating embeddings...')
    # Use HuggingFace embeddings which are free and run locally
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})

    print('Building FAISS vector store...')
    db = FAISS.from_documents(texts, embeddings)
    DB_FAISS_PATH.parent.mkdir(parents=True, exist_ok=True)
    db.save_local(str(DB_FAISS_PATH))
    print('FAISS vector store created successfully at', DB_FAISS_PATH)

if __name__ == '__main__':
    create_vector_db()