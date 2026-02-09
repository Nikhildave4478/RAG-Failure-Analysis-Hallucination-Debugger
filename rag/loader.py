# rag/loader.py
from langchain_community.document_loaders import TextLoader

def load_documents(path: str):
    loader = TextLoader(path)
    documents = loader.load()
    return documents
