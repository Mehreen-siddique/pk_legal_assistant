import os
import sys
from utils.pdf_loader import load_pdf_text
from utils.text_cleaner import clean_text
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

def main():
    """
    Orchestrates the build process:
    1. Reads all PDF files from the 'data' directory.
    2. Extracts, cleans, and splits text into chunks.
    3. Computes embeddings using paraphrase-multilingual-mpnet-base-v2.
    4. Saves the generated FAISS index locally to 'legal_faiss/'.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    db_dir = os.path.join(base_dir, "legal_faiss")
    
    print("=" * 60)
    print("STARTING FAISS VECTOR DATABASE BUILD PIPELINE")
    print("=" * 60)
    
    # Check if data directory exists
    if not os.path.exists(data_dir):
        print(f"Error: Data directory '{data_dir}' does not exist.")
        print("Please create the data directory and add legal PDF documents.")
        sys.exit(1)
        
    # List all PDF files
    pdf_files = [f for f in os.listdir(data_dir) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"Error: No PDF files found in '{data_dir}'.")
        print("Please run 'python generate_dummy_pdfs.py' to generate test data.")
        sys.exit(1)
        
    print(f"Found {len(pdf_files)} PDF files to process: {pdf_files}\n")
    
    all_documents = []
    
    # Configure chunking strategy
    # chunk_size = 1000, chunk_overlap = 200 as specified
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(data_dir, pdf_file)
        print(f"Loading and processing: {pdf_file}...")
        
        try:
            # 1. Load PDF Text
            raw_text = load_pdf_text(pdf_path)
            
            # 2. Clean Text
            cleaned_text = clean_text(raw_text)
            
            # 3. Chunk Text
            chunks = splitter.split_text(cleaned_text)
            print(f"-> Extracted {len(chunks)} chunks.")
            
            # 4. Convert chunks to Document objects with metadata
            doc_title = pdf_file.replace(".pdf", "").replace("_", " ").title()
            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": pdf_file,
                        "chunk_index": i,
                        "title": doc_title
                    }
                )
                all_documents.append(doc)
                
        except Exception as e:
            print(f"Error processing {pdf_file}: {str(e)}")
            print("Skipping this file...\n")
            
    if not all_documents:
        print("\nError: No text chunks extracted. FAISS database build aborted.")
        sys.exit(1)
        
    print(f"\nTotal extracted chunks across all files: {len(all_documents)}")
    print("Loading multilingual embedding model...")
    print("Model: sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
    
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        print("Generating embeddings and building FAISS vector store...")
        db = FAISS.from_documents(all_documents, embeddings)
        
        print(f"Saving FAISS database locally to '{db_dir}'...")
        os.makedirs(db_dir, exist_ok=True)
        db.save_local(db_dir)
        
        print("=" * 60)
        print("FAISS VECTOR DATABASE BUILT AND SAVED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError building or saving FAISS database: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
