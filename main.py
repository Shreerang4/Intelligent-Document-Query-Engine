import fitz
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
import asyncio
import time
import gc

load_dotenv()

# --- Pydantic Models for API (This was the missing part) ---
class QueryRequest(BaseModel):
    documents: HttpUrl
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

# --- FastAPI App Initialization ---
app = FastAPI(title="Intelligent Query–Retrieval System", version="1.0.0")
EXPECTED_TOKEN = "b67c9abf3c4db8e30556bc012a00cdb3f4072ccd6502a59372dc1aa1cc24f14d"

# --- Model Cache ---
model_cache = {}

def get_embedding_model():
    """Loads the embedding model from cache or initializes it."""
    if "embedding_model" not in model_cache:
        print("Loading embedding model for the first time...")
        model_cache["embedding_model"] = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return model_cache["embedding_model"]

def get_reranker_model():
    """Loads the reranker model from cache or initializes it."""
    if "reranker" not in model_cache:
        print("Loading reranker model for the first time...")
        model_cache["reranker"] = CrossEncoder('cross-encoder/ms-marco-TinyBERT-L-2-v2')
    return model_cache["reranker"]

# --- RAG Core Logic Functions ---
def load_and_chunk_pdf(url: str):
    # (This function remains the same)
    print(f"Loading document from: {url}")
    try:
        response = requests.get(url, timeout=30)  # Add timeout
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to download document: {e}")
    full_text = ""
    try:
        with fitz.open(stream=response.content, filetype="pdf") as doc:
            for page in doc:
                blocks = page.get_text("blocks")
                blocks.sort(key=lambda b: (b[1], b[0]))
                for b in blocks: full_text += b[4]
        print("Document loaded and parsed successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {e}")
    
    # Use smaller chunks to reduce memory usage
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = text_splitter.split_text(full_text)
    print(f"Document split into {len(chunks)} chunks.")
    return chunks

def create_vector_store(chunks: list[str], embedding_model):
    # (This function remains the same)
    if not chunks: raise HTTPException(status_code=400, detail="No text chunks to process.")
    print("Creating embeddings...")
    chunk_embeddings = embedding_model.embed_documents(chunks)
    embedding_array = np.array(chunk_embeddings).astype('float32')
    index = faiss.IndexFlatL2(embedding_array.shape[1])
    index.add(embedding_array)
    print(f"FAISS index created with {index.ntotal} vectors.")
    return index

def generate_final_answer(question: str, context: str):
    # (This function remains the same)
    print("Generating final answer with LLM...")
    try:
        client = Groq()
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an AI assistant. Answer the user's question based ONLY on the provided context. Be concise and precise. If the answer is not in the document, say that."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
            ],
            model="llama3-8b-8192",
            timeout=90  # Increased timeout for 10 questions
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error during LLM call: {e}")
        return "Error generating the final answer."

# --- API Endpoint ---
@app.post("/hackrx/run", response_model=QueryResponse)
async def run_query_pipeline(request: QueryRequest, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer ") or authorization.split("Bearer ")[1] != EXPECTED_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authorization token")
    
    start_time = time.time()
    print(f"Starting processing at {start_time}")
    
    try:
        # Allow up to 10 questions for hackathon requirements
        if len(request.questions) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 questions allowed per request")
        
        print(f"Processing {len(request.questions)} questions...")
        
        # Load models once and reuse
        embedding_model = get_embedding_model()
        reranker = get_reranker_model()

        # Process document once and reuse for all questions
        doc_chunks = load_and_chunk_pdf(str(request.documents))
        faiss_index = create_vector_store(doc_chunks, embedding_model)
        
        final_answers = []
        for i, question in enumerate(request.questions):
            print(f"\nProcessing question {i+1}/{len(request.questions)}: '{question}'")
            
            try:
                question_embedding = embedding_model.embed_query(question)
                question_embedding_np = np.array([question_embedding]).astype('float32')
                k_initial = 5  # Keep this optimized for memory
                distances, indices = faiss_index.search(question_embedding_np, k_initial)
                retrieved_chunks = [doc_chunks[i] for i in indices[0]]
                
                rerank_pairs = [[question, chunk] for chunk in retrieved_chunks]
                rerank_scores = reranker.predict(rerank_pairs)
                reranked_results = sorted(zip(retrieved_chunks, rerank_scores), key=lambda x: x[1], reverse=True)
                
                top_k_final = 2  # Keep this optimized for memory
                final_context = "\n\n".join([chunk for chunk, score in reranked_results[:top_k_final]])
                answer = generate_final_answer(question, final_context)
                final_answers.append(answer)
                
                print(f"Completed question {i+1} in {time.time() - start_time:.2f}s")
                
            except Exception as e:
                print(f"Error processing question {i+1}: {e}")
                final_answers.append(f"Error processing question: {str(e)}")
            
            # Force garbage collection after each question to manage memory
            gc.collect()

        total_time = time.time() - start_time
        print(f"Total processing time: {total_time:.2f}s")
        return QueryResponse(answers=final_answers)
        
    except Exception as e:
        print(f"Error in processing: {e}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

# Add a health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "RAG system is running"}