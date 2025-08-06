import fitz  # PyMuPDF
import faiss
import numpy as np
import os
from groq import Groq
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder

def load_and_chunk_pdf(file_path: str):
    """Loads a local PDF using a layout-aware method and chunks it."""
    print(f"Loading document from: {file_path}")
    full_text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                blocks = page.get_text("blocks")
                blocks.sort(key=lambda b: (b[1], b[0]))
                for b in blocks:
                    full_text += b[4]
        print("Document loaded successfully.")
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return []

    print("Chunking document...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_text(full_text)
    print(f"Document split into {len(chunks)} chunks.")
    return chunks

def create_vector_store(chunks: list[str], embedding_model):
    """Creates embeddings and builds a FAISS index."""
    if not chunks:
        print("No chunks to process. Exiting.")
        return None
        
    print("Creating embeddings... (This may take a moment)")
    try:
        chunk_embeddings = embedding_model.embed_documents(chunks)
    except Exception as e:
        print(f"Error creating embeddings: {e}")
        return None
    
    embedding_array = np.array(chunk_embeddings).astype('float32')
    index = faiss.IndexFlatL2(embedding_array.shape[1])
    index.add(embedding_array)
    
    print(f"FAISS index created successfully with {index.ntotal} vectors.")
    return index

def generate_final_answer(question: str, context: str):
    """Uses an LLM to generate a final, clean answer from the context."""
    print("\nGenerating final answer with LLM...")
    try:
        # API key is read automatically from the .env file
        client = Groq() 
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant. Answer the user's question based ONLY on the provided context. Be concise and precise. If the answer is not in the context, say that you cannot find the answer in the document."
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
        return f"Error generating answer: {e}"

if __name__ == "__main__":
    load_dotenv() # Load variables from .env file
    
    # IMPORTANT: Make sure this path is correct
    pdf_file_path = "C:/Users/Dell/Downloads/Recipe-Book.pdf"
    
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    doc_chunks = load_and_chunk_pdf(pdf_file_path)
    faiss_index = create_vector_store(doc_chunks, embedding_model)

    if faiss_index:
        reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        user_question = "Give me recipe to make the fastest pickle.Also give me recipe for the slowest pickle to make.Also give me recipe for something not too oily but not too healthy also."
        
        print(f"\nSearching for chunks relevant to: '{user_question}'")
        
        question_embedding = embedding_model.embed_query(user_question)
        question_embedding_np = np.array([question_embedding]).astype('float32')

        k_initial = 10 
        distances, indices = faiss_index.search(question_embedding_np, k_initial)
        retrieved_chunks = [doc_chunks[i] for i in indices[0]]
        
        print("Reranking retrieved chunks...")
        rerank_pairs = [[user_question, chunk] for chunk in retrieved_chunks]
        rerank_scores = reranker.predict(rerank_pairs)
        reranked_results = sorted(zip(retrieved_chunks, rerank_scores), key=lambda x: x[1], reverse=True)

        # Combine the top reranked chunks into a single context
        top_k_final = 3
        final_context = "\n\n".join([chunk for chunk, score in reranked_results[:top_k_final]])

        # Generate the final answer using the LLM
        final_answer = generate_final_answer(user_question, final_context)

        # Print the final, clean answer
        print("\n" + "="*40)
        print("✅ FINAL ANSWER:")
        print("="*40)
        print(final_answer)