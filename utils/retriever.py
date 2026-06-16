import os
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Absolute path to legal_faiss folder
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_DIR = os.path.join(BASE_DIR, "legal_faiss")

@st.cache_resource
def get_embeddings_model() -> HuggingFaceEmbeddings:
    """
    Loads and caches the paraphrase-multilingual-mpnet-base-v2 model
    to perform semantic search in English, Roman Urdu, and Urdu.
    """
    model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    print(f"Loading embedding model: {model_name}...")
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'} # Can force CPU for embeddings as it's lightweight
    )

@st.cache_resource
def load_vector_db() -> FAISS:
    """
    Loads and caches the FAISS vector database.
    Raises FileNotFoundError if index does not exist.
    """
    embeddings = get_embeddings_model()
    
    index_file = os.path.join(DB_DIR, "index.faiss")
    pkl_file = os.path.join(DB_DIR, "index.pkl")
    
    if not os.path.exists(index_file) or not os.path.exists(pkl_file):
        raise FileNotFoundError(
            f"FAISS index files not found in '{DB_DIR}'. "
            "Please run 'python build_vector_db.py' to build the vector store."
        )
        
    try:
        # allow_dangerous_deserialization is required to load FAISS pickle files locally
        db = FAISS.load_local(DB_DIR, embeddings, allow_dangerous_deserialization=True)
        return db
    except Exception as e:
        print(f"Failed to load FAISS index: {str(e)}")
        raise RuntimeError(f"Error loading vector store: {str(e)}")

def retrieve_documents(query: str, k: int = 5):
    """
    Performs similarity search on FAISS database and returns the top k chunks.
    
    Args:
        query (str): The search query.
        k (int): Number of documents to retrieve.
        
    Returns:
        List[Document]: List of LangChain Document objects.
    """
    try:
        db = load_vector_db()
        return db.similarity_search(query, k=k)
    except Exception as e:
        print(f"Retrieval error: {str(e)}")
        raise RuntimeError(f"Failed to retrieve documents: {str(e)}")
