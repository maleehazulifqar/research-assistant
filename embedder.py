from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from loader import load_and_split
import os

def get_embeddings():
    return HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",
        huggingfacehub_api_token=os.environ.get("HF_TOKEN")
    )

def create_vectorstore(file_paths):
    embeddings = get_embeddings()
    if isinstance(file_paths, str):
        file_paths = [file_paths]
    all_chunks = []
    for path in file_paths:
        chunks = load_and_split(path)
        all_chunks.extend(chunks)
    return FAISS.from_texts(all_chunks, embeddings)

def save_vectorstore(vectorstore, path="vectorstore"):
    vectorstore.save_local(path)

def load_vectorstore(path="vectorstore"):
    embeddings = get_embeddings()
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)