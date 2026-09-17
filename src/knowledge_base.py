import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DB_FAISS_PATH = 'vectorstore/db_faiss'
DATA_PATH = 'data/'

def create_vector_db():
    print('Loading documents...')
    loader = DirectoryLoader(DATA_PATH, glob='*.txt', loader_cls=TextLoader)
    documents = loader.load()
    print(f'Loaded {len(documents)} documents.')

    print('Splitting text...')
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    print('Creating embeddings...')
    # Use HuggingFace embeddings which are free and run locally
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})

    print('Building FAISS vector store...')
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)
    print('FAISS vector store created successfully at', DB_FAISS_PATH)

if __name__ == '__main__':
    create_vector_db()