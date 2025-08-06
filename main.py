import fitz  # PyMuPDF
import faiss
import numpy as np
import os
import requests
from groq import Groq
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder

# --- Load Environment Variables ---
load_dotenv()

# --- Pydantic Models for API ---
class QueryRequest(BaseModel):
    documents: HttpUrl
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Intelligent Query–Retrieval System",
    description="An API to answer questions about documents using RAG.",
    version="1.0.0"
)

EXPECTED_TOKEN = "b67c9abf3c4db8e30556bc012a00cdb3f4072ccd6502a59372dc1aa1cc24f14d"

# --- RAG Core Logic Functions ---

def load_and_chunk_pdf(url: str):
    """Downloads a PDF from a URL, extracts text, and chunks it."""
    print(f"Loading document from: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to download document: {e}")

    full_text = ""
    try:
        with fitz.open(stream=response.content, filetype="pdf") as doc:
            for page in doc:
                blocks = page.get_text("blocks")
                blocks.sort(key=lambda b: (b[1], b[0]))
                for b in blocks:
                    full_text += b[4]
        print("Document loaded and parsed successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {e}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(full_text)
    print(f"Document split into {len(chunks)} chunks.")
    return chunks

def create_vector_store(chunks: list[str], embedding_model):
    """Creates embeddings and builds a FAISS index."""
    if not chunks:
        raise HTTPException(status_code=400, detail="No text chunks to process.")
    
    print("Creating embeddings... (This may take a moment)")
    chunk_embeddings = embedding_model.embed_documents(chunks)
    embedding_array = np.array(chunk_embeddings).astype('float32')
    index = faiss.IndexFlatL2(embedding_array.shape[1])
    index.add(embedding_array)
    print(f"FAISS index created with {index.ntotal} vectors.")
    return index

def generate_final_answer(question: str, context: str):
    """Uses an LLM to generate a final, clean answer from the context."""
    print("Generating final answer with LLM...")
    try:
        client = Groq()
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant. Answer the user's question based ONLY on the provided context. Be concise and precise. If the answer is not in the document, say that."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}",
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error during LLM call: {e}")
        return "There was an error generating the final answer. The LLM provider may be temporarily unavailable."

# --- API Endpoint ---
@app.post("/hackrx/run", response_model=QueryResponse)
async def run_query_pipeline(
    request: QueryRequest,
    authorization: Optional[str] = Header(None)
):
    # 1. Authentication
    if not authorization or not authorization.startswith("Bearer ") or authorization.split("Bearer ")[1] != EXPECTED_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authorization token")

    # --- Initialize Models (loaded once per server start, but here for simplicity) ---
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    # 2. Load and Chunk Document
    doc_chunks = load_and_chunk_pdf(str(request.documents))
    
    # 3. Create Vector Store
    faiss_index = create_vector_store(doc_chunks, embedding_model)
    
    final_answers = []
    # 4. Loop Through Questions
    for question in request.questions:
        print(f"\nProcessing question: '{question}'")
        
        # 5. Retrieve
        question_embedding = embedding_model.embed_query(question)
        question_embedding_np = np.array([question_embedding]).astype('float32')
        k_initial = 10
        distances, indices = faiss_index.search(question_embedding_np, k_initial)
        retrieved_chunks = [doc_chunks[i] for i in indices[0]]
        
        # 6. Rerank
        rerank_pairs = [[question, chunk] for chunk in retrieved_chunks]
        rerank_scores = reranker.predict(rerank_pairs)
        reranked_results = sorted(zip(retrieved_chunks, rerank_scores), key=lambda x: x[1], reverse=True)
        
        # 7. Generate
        top_k_final = 3
        final_context = "\n\n".join([chunk for chunk, score in reranked_results[:top_k_final]])
        answer = generate_final_answer(question, final_context)
        final_answers.append(answer)

    return QueryResponse(answers=final_answers)