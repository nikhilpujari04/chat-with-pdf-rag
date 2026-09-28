# 📄 Chat With PDF — RAG Document Intelligence System

> A production-style AI application that lets you chat with any PDF using natural language — powered by Retrieval-Augmented Generation (RAG).

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-latest-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)
![Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-orange?logo=google)
![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-purple)

---

## 🚀 Live Demo
> Deployment coming soon

---

## 🧠 What is this?

Chat With PDF is a full-stack RAG (Retrieval-Augmented Generation) application where users upload PDF documents and interact with them through natural language. Instead of relying on an LLM's training knowledge, the system retrieves the most relevant chunks from the actual document and grounds every answer in real content — with source page citations.

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 **Ask Document** | Ask any question — get grounded answers with page citations |
| 📝 **Summarize PDF** | Generate a concise document summary instantly |
| 🔑 **Extract Key Points** | Pull out important facts as a structured bullet list |
| 🎓 **Explain Like Beginner** | Complex topics simplified in plain language |
| 🎮 **Quiz Game** | AI-generated interactive quiz with scoring and feedback |
| 🌙 **Dark / Light Theme** | Full theme toggle with persistent state |
| ⚙️ **Settings Panel** | Live-tunable retrieval and LLM parameters |

---

## 🏗️ Architecture

```
PDF Upload
    ↓
PDF Text Extraction (PyPDF)
    ↓
Document Chunking (RecursiveCharacterTextSplitter)
    ↓
Text Embeddings (sentence-transformers/all-MiniLM-L6-v2)
    ↓
FAISS Vector Store (saved to disk)
    ↓
User Question
    ↓
Hybrid Retrieval (BM25 + FAISS → EnsembleRetriever)
    ↓
Grounded Prompt (context + question → Gemini)
    ↓
Answer + Page Citations
```

---

## 🗂️ Project Structure

```
chat-with-pdf-rag/
│
├── app.py                    # Streamlit entry point
├── requirements.txt          # All dependencies
├── .env.example              # Template for environment variables
├── README.md
│
├── src/                      # Core RAG pipeline
│   ├── config.py             # Centralized settings
│   ├── logger.py             # Logging setup
│   ├── pdf_loader.py         # PDF text extraction
│   ├── text_splitter.py      # Document chunking
│   ├── embeddings.py         # Embedding model (MiniLM)
│   ├── vector_store.py       # FAISS + hybrid retriever
│   └── rag_chain.py          # LLM prompt templates + query functions
│
├── ui/                       # Streamlit UI components
│   ├── styles.py             # Theme-aware CSS + particle animation
│   ├── sidebar.py            # Sidebar navigation
│   └── views/                # One file per view
│       ├── welcome.py
│       ├── chat.py
│       ├── document.py
│       ├── quiz.py
│       ├── settings.py
│       └── help.py
│
└── data/                     # Runtime data (gitignored)
    ├── uploads/              # Uploaded PDFs
    └── vector_store/         # Saved FAISS index
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| LLM | Google Gemini 2.5 Flash |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | FAISS (Facebook AI Similarity Search) |
| Keyword Search | BM25 (rank-bm25) |
| Retrieval | LangChain EnsembleRetriever (Hybrid) |
| PDF Extraction | PyPDF |
| Text Splitting | LangChain RecursiveCharacterTextSplitter |
| Frontend | Streamlit |
| Framework | LangChain |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Google Gemini API key — [get one free here](https://aistudio.google.com/)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/nikhilpujari04/chat-with-pdf-rag.git
cd chat-with-pdf-rag

# 2. Create and activate virtual environment
python -m venv venv

# Windows
.\venv\Scripts\Activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 5. Run the app
streamlit run app.py
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

## ⚠️ Known Limitations

- Scanned / image-based PDFs are not supported (no OCR)
- Very large documents (100+ pages) may truncate in summary modes
- Retrieval quality depends on question phrasing — rephrase if answer seems wrong
- Heavily designed PDF templates (Canva etc.) may extract with spacing issues

---

## 🔮 Future Improvements

- [ ] Multi-PDF support (combined knowledge base)
- [ ] OCR support for scanned PDFs
- [ ] Streaming LLM responses
- [ ] Map-reduce summarization for large documents
- [ ] Deployment on Streamlit Cloud
- [ ] Persistent vector store (Pinecone / pgvector)
- [ ] Re-ranking with cross-encoder models

---

## 👤 Author

**Nikhil Pujari**
- 📧 pujarinikhil04@gmail.com
- 🎓 B.Sc. Data Science — Valia College, Mumbai
- 🔗 [GitHub](https://github.com/nikhilpujari04)

---

## 📄 License

MIT License — feel free to use, modify, and distribute.