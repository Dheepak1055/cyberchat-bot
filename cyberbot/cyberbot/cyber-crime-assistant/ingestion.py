import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Define paths
DOCS_PATH = "./documents/"
DB_PATH = "./chroma_db"

def main():
    """
    Main function to run the entire data ingestion pipeline.
    """
    # Force re-creation of the vector store by deleting the old one
    if os.path.exists(DB_PATH):
        print("Existing vector store found. Deleting it to re-ingest data...")
        shutil.rmtree(DB_PATH)
        print("Old vector store deleted.")

    print("Creating new vector store...")
    
    # 1. Load documents
    documents = load_documents()
    
    if not documents:
        print("No PDF documents found in the 'documents' folder. Aborting.")
        return

    # 2. Split documents into chunks
    chunks = split_documents(documents)
    
    # 3. Get embedding model
    embeddings = get_embedding_model()
    
    # 4. Create and persist the vector store
    vectorstore = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=DB_PATH
    )
    print("Vector store created and persisted.")

def load_documents():
    """Loads all PDF documents from the specified directory."""
    documents = []
    if not os.path.exists(DOCS_PATH):
        print(f"Error: The directory '{DOCS_PATH}' does not exist.")
        return documents

    for filename in os.listdir(DOCS_PATH):
        if filename.endswith(".pdf"):
            filepath = os.path.join(DOCS_PATH, filename)
            loader = PyPDFLoader(filepath)
            documents.extend(loader.load())
    print(f"Loaded {len(documents)} pages from PDF files.")
    return documents

def split_documents(documents):
    """Splits the loaded documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")
    return chunks

def get_embedding_model():
    """Loads the embedding model."""
    model_name = "BAAI/bge-m3"
    # CHANGE 1: Use 'cuda' for GPU, or keep 'cpu' if a GPU is not present/available.
    model_kwargs = {'device': 'cuda'}
    encode_kwargs = {'normalize_embeddings': True}
    
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    print("Embedding model loaded.")
    return embeddings

if __name__ == "__main__":
    main()

