# Intelligent Document Query Engine

A **cloud-native, LLM-powered query-retrieval system** designed to perform **contextual analysis** on large, unstructured documents. Built for scalable, production-ready deployments.

## 🚀 Features

* **Retrieval-Augmented Generation (RAG)** pipeline using:

  * **`faiss-cpu`** for efficient vector indexing
  * **`sentence-transformers` CrossEncoder** for high-precision reranking
* **Llama 3 LLM integration** via the **Groq API** for final answer synthesis
* **Fine-tuned role-based system prompt** for domain-specific query responses
* **Lazy-loading pattern** for large AI models to optimize memory and performance
* **FastAPI backend** with REST endpoints for document ingestion and query answering
* **Docker-based deployment** for reproducibility and scalability

## 🌐 Live Demo

The application is deployed on **Railway** and available here:
[API Documentation (Swagger UI)](https://bajajhack-production-cf2c.up.railway.app/docs)

## 📂 Project Structure

```
├── main.py                 # FastAPI entry point
├── requirements.txt        # Dependencies
├── Dockerfile              # Container build setup
├── start.py / start.sh     # Application startup scripts
├── test_*.py               # API test scripts
└── deploy.sh / deploy.bat  # Deployment scripts
```

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/intelligent-document-query-engine.git
   cd intelligent-document-query-engine
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   Create a `.env` file with:

   ```
   GROQ_API_KEY=your_groq_api_key
   ```

4. **Run locally**

   ```bash
   uvicorn main:app --reload
   ```

## ☁️ Deployment

This project supports Railway deployment (Docker-based):

```bash
railway up
```

or locally via Docker:

```bash
docker build -t doc-query-engine .
docker run -p 8000:8000 doc-query-engine
```

## 📈 Performance Optimizations

* Lazy loading of embedding and reranker models
* FAISS in-memory index creation for efficient retrieval
* Batched query processing for speed
* Role-based prompts to reduce token usage

## 🧠 Tech Stack

* **Backend:** Python, FastAPI
* **Vector Indexing:** FAISS
* **LLM API:** Groq (Llama 3)
* **Reranking:** SentenceTransformers CrossEncoder
* **Deployment:** Docker, Railway

---

If you want, I can now **clean `main.py` to remove all hackathon-specific code** so the logic is consistent with this general-purpose README.
Do you want me to proceed with that cleanup?
