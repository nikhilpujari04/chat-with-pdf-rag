# Chat with PDF - RAG Application

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their content using Google's Gemini LLM.

## Features

- Upload and process PDF documents
- Extract and chunk text intelligently
- Build semantic search indexes using FAISS
- Query documents using natural language
- Powered by Google's Gemini 2.5 Flash model
- Streamlit UI for easy interaction

## Project Structure

```
chat-with-pdf-rag/
├── .env                      # API keys (never committed to GitHub)
├── .gitignore                # ignore venv, .env, __pycache__, etc.
├── requirements.txt          # pinned dependencies
├── README.md                 # project documentation
├── app.py                    # Streamlit entry point (UI)
├── src/
│   ├── __init__.py
│   ├── config.py             # loads env vars, central settings
│   ├── pdf_loader.py         # extract text from PDFs
│   ├── text_splitter.py      # chunking logic
│   ├── embeddings.py         # embedding model setup
│   ├── vector_store.py       # FAISS build/load/save
│   ├── rag_chain.py          # retrieval + Gemini LLM chain
│   └── logger.py             # logging setup
├── data/
│   ├── uploads/              # uploaded PDFs (gitignored)
│   └── vector_store/         # saved FAISS index (gitignored)
└── logs/                     # log files (gitignored)
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd chat-with-pdf-rag
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

5. Run the application:
```bash
streamlit run app.py
```

## Configuration

All configuration is managed through `src/config.py` which loads from `.env`. Key settings:

- `GOOGLE_API_KEY` - Your Google Generative AI API key
- `LLM_MODEL` - Model to use (default: gemini-2.5-flash)
- `EMBEDDING_MODEL` - Sentence transformer model (default: all-MiniLM-L6-v2)
- `CHUNK_SIZE` - Text chunk size for splitting (default: 1000)
- `CHUNK_OVERLAP` - Overlap between chunks (default: 200)

## Usage

1. Launch the Streamlit app
2. Upload PDF documents using the file uploader
3. Ask questions about the content
4. The RAG system retrieves relevant chunks and generates answers using Gemini

## Components

### `config.py`
Central configuration management. Loads environment variables and provides default values.

### `pdf_loader.py`
Handles PDF file reading and text extraction using PyPDF2.

### `text_splitter.py`
Implements recursive character splitting for efficient chunking with overlap.

### `embeddings.py`
Manages the embedding model (SentenceTransformer) for converting text to vectors.

### `vector_store.py`
FAISS vector store operations - creating, saving, loading, and searching indexes.

### `rag_chain.py`
Orchestrates the RAG pipeline: retrieval + LLM query generation.

### `logger.py`
Centralized logging configuration for debugging and monitoring.

### `app.py`
Streamlit frontend - file upload, chat interface, and result display.

## API Keys

To use this application, you need a Google Generative AI API key:

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create or copy your API key
3. Add it to your `.env` file as `GOOGLE_API_KEY`

## Error Handling

The application includes:
- Retry logic with exponential backoff for API rate limits
- Graceful error messages in the UI
- Detailed logging for debugging

## Future Enhancements

- Support for multiple document types (DOCX, TXT, etc.)
- Conversation memory/history
- Document summarization
- Multi-language support
- Web scraping for content addition
- Custom prompt templates

## License

MIT

## Support

For issues or questions, please open an issue on GitHub.
