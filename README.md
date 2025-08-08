# Bajaj Hackathon RAG API

A FastAPI-based Retrieval-Augmented Generation (RAG) system that can answer questions from insurance policy documents. The system is optimized for hackathon requirements and can handle up to 10 questions per request.

## 🚀 Features

- **Document Processing**: Supports PDF documents from URLs
- **Question Answering**: Handles up to 10 questions per request
- **RAG Pipeline**: Uses embedding models, FAISS vector search, and LLM generation
- **Memory Optimized**: Efficient memory management for large document processing
- **Production Ready**: Deployed on Railway with health checks

## 📋 Hackathon Requirements

The system now supports the full hackathon evaluation with 10 comprehensive questions:

1. Grace period for premium payment
2. Waiting period for pre-existing diseases
3. Coverage limits for medical expenses
4. Policy term and renewal process
5. Exclusions and limitations
6. Claim settlement process
7. Premium payment options
8. Hospitalization coverage and room rent
9. Outpatient treatment benefits
10. Family member management process

## 🛠️ API Endpoints

### Main Endpoint
```
POST /hackrx/run
```

**Headers:**
```
Authorization: Bearer b67c9abf3c4db8e30556bc012a00cdb3f4072ccd6502a59372dc1aa1cc24f14d
Content-Type: application/json
```

**Request Body:**
```json
{
  "documents": "https://example.com/policy.pdf",
  "questions": [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?"
  ]
}
```

**Response:**
```json
{
  "answers": [
    "The grace period is 30 days...",
    "The waiting period is 48 months..."
  ]
}
```

### Health Check
```
GET /health
```

## 🧪 Testing

### Python Test
```bash
python test_hackathon.py
```

### PowerShell Test
```powershell
.\test_hackathon.ps1
```

### Simple Test (2 questions)
```bash
python test_api.py
```

## 🚀 Deployment

### Using Railway CLI

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Windows:**
```cmd
deploy.bat
```

### Manual Deployment
```bash
railway up
```

## 📊 Performance Optimizations

- **Memory Management**: Garbage collection after each question
- **Model Caching**: Embedding and reranker models cached in memory
- **Document Processing**: Single document processing for multiple questions
- **Timeout Handling**: 90-second timeout per LLM call
- **Error Handling**: Graceful error handling for individual questions

## 🔧 Technical Stack

- **FastAPI**: Web framework
- **PyMuPDF**: PDF processing
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Embedding models
- **Groq**: LLM API for answer generation
- **Railway**: Deployment platform

## 📈 Recent Updates

- ✅ Removed 5-question limit
- ✅ Added support for 10 questions
- ✅ Optimized memory usage
- ✅ Enhanced error handling
- ✅ Created comprehensive test suite
- ✅ Added deployment scripts

## 🎯 Hackathon Ready

The system is now fully optimized for hackathon evaluation with:
- Support for 10 questions per request
- Comprehensive error handling
- Performance monitoring
- Easy deployment and testing
- Production-ready API endpoints

## 📞 Support

For hackathon-related issues or questions, refer to the test files and deployment scripts provided.