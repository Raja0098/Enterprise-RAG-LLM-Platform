# 🚀 Enterprise RAG LLM Platform

Plug-and-play enterprise-grade Retrieval-Augmented Generation (RAG) platform that allows organizations to ingest documents, define rules, and deploy a domain-restricted AI assistant.

Designed for production use with context-aware retrieval, query expansion, reranking, and conversational memory.

---

## 🧠 Overview

This system enables companies to:

- Upload and ingest internal documents
- Ask domain-specific questions
- Get accurate, grounded responses (no hallucination)
- Maintain conversational context across sessions
- Enforce rule-based response control

The platform ensures answers are **strictly derived from provided data**, making it suitable for enterprise environments.

---

## ⚙️ Key Features

- 🔌 **Plug-and-Play Architecture** – Easily integrate with any company dataset  
- 📄 **Document Ingestion Pipeline** – Process PDFs, text, and structured data  
- 🧠 **Context-Aware Query Rewriting** – Uses conversation history for better retrieval  
- 🔍 **Multi-Query Retrieval** – Improves recall and search accuracy  
- ⚡ **Cross-Encoder Reranking** – Enhances relevance using BGE reranker  
- 🧾 **Rule-Based Response Control** – Prevents hallucination  
- 💬 **Session-Based Memory** – Maintains conversational context (PostgreSQL)  
- 📦 **Vector Search (Milvus)** – Fast and scalable similarity search  
- 🌐 **Full-Stack Application** – FastAPI backend + Vue.js frontend  

---

## 🏗️ System Architecture

User Query
   ↓
Intent Classification
   ↓
Query Expansion (LLM)
   ↓
Embedding Generation
   ↓
Vector Search (Milvus)
   ↓
Reranking (CrossEncoder)
   ↓
Context Construction
   ↓
LLM Response Generation
   ↓
Conversation Memory (Postgres)



---

## 🧪 Tech Stack

- **Backend:** FastAPI, Python  
- **LLM:** Gemini API  
- **Embeddings:** Gemini Embeddings  
- **Vector DB:** Milvus  
- **Reranking:** Sentence Transformers (BAAI/bge-reranker)  
- **Database:** PostgreSQL  
- **Frontend:** Vue.js  
- **Other:** Docker (optional), REST APIs  

---
