# Research Assistant — AI-Powered PDF Q&A

> Upload any research paper and ask questions about it in natural language.

**Live Demo:** [clever-illumination-production.up.railway.app](https://clever-illumination-production.up.railway.app)

---

## Overview

Research Assistant is an AI-powered tool built on **Retrieval Augmented Generation (RAG)**. Upload one or more research PDFs, and the assistant retrieves only the relevant content to answer your questions accurately — no hallucinations, no guessing.



## Features

- Upload single or multiple research PDFs
- Ask natural language questions across all documents
- RAG pipeline grounds every answer in the actual document
- Chat history — the assistant remembers previous questions
- Fast inference via Groq (LLaMA 3)
- Free embeddings via HuggingFace — no OpenAI key needed
- Clean, minimal UI built with Flask + HTML/CSS
- Deployed on Railway

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | LLaMA 3 via Groq API |
| Orchestration | LangChain |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | FAISS (local) |
| PDF Parsing | pdfplumber |
| Backend | Flask |
| Frontend | HTML / CSS / Vanilla JS |
| Deployment | Railway |

---

## How RAG Works

```
PDF Upload
    ↓
Text Extraction  (pdfplumber)
    ↓
Chunking  (RecursiveCharacterTextSplitter)
    ↓
Embeddings  (HuggingFace)
    ↓
Vector Store  (FAISS)
    ↓
User Question
    ↓
Similarity Search → Top 3 Relevant Chunks Retrieved
    ↓
LLaMA 3 via Groq generates answer from context
    ↓
Answer displayed in UI
```

---

## Project Structure

```
research-assistant/
│
├── Server.py          # Flask backend API
├── embedder.py        # Embeddings + FAISS vector store
├── retriever.py       # RAG chain with Groq LLM
├── loader.py          # PDF loading and chunking
├── index.html         # Frontend UI
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container configuration
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/maleehazulifqar/research-assistant.git
cd research-assistant
```

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 5. Run locally

```bash
python Server.py
```

Open: `http://127.0.0.1:5000`

---

## Usage

1. Click **"Click to upload PDFs"** in the sidebar
2. Select one or more research papers
3. Click **"Process Documents"** — wait for "Document ready"
4. Type your question and press **Enter**

---

## Deployment

This project is deployed on **Railway** using Docker.

To deploy your own instance:

1. Fork this repository
2. Create a new project on [railway.app](https://railway.app)
3. Connect your GitHub repo
4. Add `GROQ_API_KEY` as an environment variable
5. Deploy!

---

## Dependencies

```
flask
langchain
langchain-groq
langchain-community
langchain-text-splitters
pdfplumber
faiss-cpu
python-dotenv
tiktoken
sentence-transformers
```

---

## Future Improvements

- Multi-PDF cross-document querying
- Source highlighting — show which chunk was used
- Citation generation with page numbers
- Persistent vector store across deployments
- User authentication

