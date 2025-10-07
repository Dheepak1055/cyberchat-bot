# main.py

from langchain_community.llms import Ollama 
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# --- Configuration ---
# Define paths and model details
DB_PATH = "./chroma_db"
EMBEDDING_MODEL_NAME = "BAAI/bge-m3"
OLLAMA_MODEL_NAME = "phi3:mini" # Specify the Ollama model



# This is the function you need to fix
def load_llm():
    """
    Loads the specified Ollama model.
    Using 'num_gpu=-1' attempts to offload all layers to the GPU.
    Requires a working Ollama server installation with GPU support.
    """
    print(f"Loading Ollama model: {OLLAMA_MODEL_NAME} with GPU offloading...")
    llm = Ollama(
        model=OLLAMA_MODEL_NAME,
        temperature=0.1, # Lower temperature for more deterministic, factual answers
        num_gpu=-1 # CHANGE 3: Explicitly enable GPU offloading for Ollama
    )
    print("LLM loaded successfully.")
    return llm

def get_embedding_model():
    """
    Loads the embedding model from Hugging Face.
    This MUST be the same model used in ingestion.py.
    """
    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        # CHANGE 2: Use 'cuda' for GPU
        model_kwargs={'device': 'cuda'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("Embedding model loaded.")
    return embeddings

def create_prompt_template():
    """
    Creates the prompt template with strict instructions for the LLM.
    [cite_start]This is taken directly from the guide[cite: 129, 133].
    """
    template = """
    You are a specialized assistant for Cyber Crime Investigation Officers. Your sole purpose is to provide accurate, step-by-step guidance based *exclusively* on the provided context from the official investigation manuals.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    INSTRUCTIONS:
    1. [cite_start]Analyze the provided CONTEXT and answer the QUESTION based *only* on this information[cite: 130].
    2. [cite_start]Do not use any external knowledge or information you were pre-trained on[cite: 130].
    3. [cite_start]For every piece of information you provide, you MUST cite the source document and page number from the metadata of the context[cite: 130].
    4. [cite_start]If the provided CONTEXT does not contain enough information to answer the question, you MUST respond with: "I do not have enough information in the provided manuals to answer this question." [cite: 131]
    5. Structure your answers clearly. [cite_start]If the question asks for a procedure, provide a step-by-step list[cite: 132].
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    return prompt

def create_rag_chain():
    """
    [cite_start]Creates and returns the complete RAG chain[cite: 147].
    """
    # Load components
    llm = load_llm()
    embeddings = get_embedding_model()
    prompt = create_prompt_template()

    # Load the persisted vector store
    print("Loading vector store...")
    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    print("Vector store loaded.")

    # Create a retriever from the vector store
    # [cite_start]Retrieve top 5 most relevant chunks [cite: 148]
    retriever = vectorstore.as_retriever(search_kwargs={'k': 5})

    # Define a function to format the retrieved documents
    def format_docs(docs):
        return "\n\n".join(
            f"Content: {doc.page_content}\nMetadata: {doc.metadata}" for doc in docs
        )

    # Construct the RAG chain using LangChain Expression Language (LCEL)
    # [cite_start]This structure is based on the guide's implementation[cite: 149].
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("RAG chain created successfully.")
    return rag_chain

if __name__ == "__main__":
    # Create the RAG chain
    chain = create_rag_chain()
    
    # [cite_start]Start the interactive CLI chat loop, based on the Colab example [cite: 167, 170]
    print("\n--- Cybercrime Investigation Assistant ---")
    print("Chatbot is ready. Type 'exit' to end the conversation.")
    print("-" * 50)

    while True:
        try:
            query = input("You: ")
            if query.lower() == 'exit':
                print("Assistant: Goodbye!")
                break
            
            print("\nAssistant: Thinking...")
            response = chain.invoke(query)
            print("\nAssistant:\n", response)
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nAssistant: Goodbye!")

            break
