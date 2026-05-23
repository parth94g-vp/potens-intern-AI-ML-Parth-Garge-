from langchain_community.document_loaders import (
    PyPDFLoader,
    DirectoryLoader
)

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

print("Loading PDFs...")

# ---------------- LOAD PDFs ----------------
loader = DirectoryLoader(
    'data',
    glob="*.pdf",
    loader_cls=PyPDFLoader
)

documents = loader.load()

print(f"Loaded {len(documents)} pages")

# ---------------- SPLIT TEXT ----------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

texts = text_splitter.split_documents(documents)

print(f"Created {len(texts)} text chunks")

# ---------------- EMBEDDINGS ----------------
print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Creating FAISS vector database...")

# ---------------- CREATE VECTOR DB ----------------
faiss_db = FAISS.from_documents(
    texts,
    embeddings
)

# ---------------- SAVE DB ----------------
faiss_db.save_local("ipc_vector_db")

print("✅ Vector database created successfully!")