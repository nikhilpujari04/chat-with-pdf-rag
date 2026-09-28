"""
Connects FAISS retrieval to the Gemini LLM.
Given a user question, retrieves the most relevant chunks,
builds a grounded prompt, and returns an answer with page citations.
"""
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.config import Config
from src.logger import get_logger

logger = get_logger(__name__)
_llm = None
MAX_CONTEXT_CHARS = 15000  # cap for whole-document modes (summarize, key points, quiz)


def _get_full_document_context(all_chunks: list[dict]) -> str:
    """
    Builds a context string from all chunks, capped at MAX_CONTEXT_CHARS.
    Used for modes that need broad document coverage (summarize, key points, quiz)
    rather than narrow question-specific retrieval.

    Note: for very large documents, this truncates rather than summarizing
    each section first (a technique called map-reduce summarization) —
    a known scaling limitation for documents beyond a few dozen pages.
    """
    full_text = "\n\n".join(chunk["chunk_text"] for chunk in all_chunks)

    if len(full_text) > MAX_CONTEXT_CHARS:
        logger.warning(
            f"Document content ({len(full_text)} chars) exceeds cap "
            f"({MAX_CONTEXT_CHARS}); truncating for this mode."
        )
        full_text = full_text[:MAX_CONTEXT_CHARS]

    return full_text
def summarize_document(all_chunks: list[dict]) -> dict:
    """Generates a summary of the entire document."""
    logger.info("Generating document summary.")
    context = _get_full_document_context(all_chunks)

    prompt = ChatPromptTemplate.from_template(SUMMARIZE_TEMPLATE)
    filled_prompt = prompt.format(context=context)

    llm = get_llm()
    response = llm.invoke(filled_prompt)

    return {"answer": response.content, "sources": []}


def extract_key_points(all_chunks: list[dict]) -> dict:
    """Extracts key points from the entire document."""
    logger.info("Extracting key points.")
    context = _get_full_document_context(all_chunks)

    prompt = ChatPromptTemplate.from_template(KEY_POINTS_TEMPLATE)
    filled_prompt = prompt.format(context=context)

    llm = get_llm()
    response = llm.invoke(filled_prompt)

    return {"answer": response.content, "sources": []}


def explain_like_beginner(retriever, question: str) -> dict:
    """Answers a question in simplified, beginner-friendly language."""
    logger.info(f"Beginner-mode question: {question}")

    retrieved_docs = retriever.invoke(question)

    if not retrieved_docs:
        return {"answer": "I couldn't find that information in the document.", "sources": []}

    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    page_numbers = sorted(set(doc.metadata["page_number"] for doc in retrieved_docs))

    prompt = ChatPromptTemplate.from_template(EXPLAIN_BEGINNER_TEMPLATE)
    filled_prompt = prompt.format(context=context, question=question)

    llm = get_llm()
    response = llm.invoke(filled_prompt)

    return {"answer": response.content, "sources": page_numbers}


def generate_quiz(all_chunks: list[dict]) -> dict:
    """
    Generates a structured 5-question quiz from the document.
    Returns parsed JSON list of questions, not raw text.
    """
    logger.info("Generating structured quiz.")
    context = _get_full_document_context(all_chunks)

    prompt = ChatPromptTemplate.from_template(QUIZ_TEMPLATE)
    filled_prompt = prompt.format(context=context)

    llm = get_llm()

    try:
        response = llm.invoke(filled_prompt)
        raw = response.content.strip()

        # Strip markdown code fences if Gemini wraps output despite instructions
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        questions = json.loads(raw)

        # Validate structure
        if not isinstance(questions, list) or len(questions) == 0:
            raise ValueError("Quiz response was not a valid list.")

        logger.info(f"Quiz generated successfully: {len(questions)} questions.")
        return {"questions": questions, "error": None}

    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Failed to parse quiz JSON: {e}\nRaw response: {raw}")
        return {"questions": None, "error": "Quiz generation failed — Gemini returned unexpected format. Try again."}
    except Exception as e:
        logger.error(f"Quiz generation error: {e}")
        return {"questions": None, "error": str(e)}  # cached singleton, same pattern as the embedding model

PROMPT_TEMPLATE = """You are a helpful assistant answering questions based ONLY on the provided context from a document.

Rules:
- Only use information found in the context below.
- If the answer is not in the context, say "I couldn't find that information in the document." Do not make up an answer.
- Be clear and concise.

Context:
{context}

Question: {question}

Answer:"""
SUMMARIZE_TEMPLATE = """You are a helpful assistant. Summarize the following document content clearly and concisely.
Focus on the main ideas, structure, and purpose of the document. Aim for 3-6 sentences unless the content clearly needs more.

Document content:
{context}

Summary:"""


KEY_POINTS_TEMPLATE = """You are a helpful assistant. Extract the most important key points from the following document content.
Present them as a clear, well-organized bullet list. Focus on facts, decisions, definitions, and figures — skip filler text.

Document content:
{context}

Key Points:"""


EXPLAIN_BEGINNER_TEMPLATE = """You are a friendly assistant explaining a document to someone with no background knowledge of the topic.

Rules:
- Only use information found in the context below.
- Avoid jargon; explain any technical terms you must use in plain language.
- Use simple sentences and, where helpful, real-world analogies.
- If the answer is not in the context, say "I couldn't find that information in the document."

Context:
{context}

Question: {question}

Beginner-friendly explanation:"""


QUIZ_TEMPLATE = """You are a quiz generator. Based on the document content below, generate exactly 5 multiple-choice questions.

CRITICAL: You must respond with ONLY a valid JSON array. No explanation, no markdown, no code blocks. Just raw JSON.

Format:
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_index": 0
  }}
]

Rules:
- correct_index is 0-based (0=A, 1=B, 2=C, 3=D)
- Questions must be based ONLY on the document content below
- Make questions genuinely challenging but fair
- Vary difficulty across the 5 questions

Document content:
{context}

JSON:"""


def get_llm() -> ChatGoogleGenerativeAI:
    """Returns a cached instance of the Gemini chat model."""
    global _llm

    if _llm is None:
        logger.info(f"Initializing Gemini model: {Config.LLM_MODEL}")
        _llm = ChatGoogleGenerativeAI(
            model=Config.LLM_MODEL,
            google_api_key=Config.GOOGLE_API_KEY
        )

    return _llm


def query_documents(retriever, question: str, k: int = 6) -> dict:
    """
    Answers a question using retrieved context from the vector store.

    Args:
        retriever: A retriever (e.g. hybrid BM25 + FAISS) used to fetch relevant chunks.
        question: The user's natural language question.
        k: How many top chunks to retrieve (used by the underlying retriever, not directly here).

    Returns:
        {
            "answer": "...",
            "sources": [1, 2, ...]   # page numbers the answer was based on
        }
    """
    logger.info(f"Received question: {question}")

    try:
        retrieved_docs = retriever.invoke(question)
    except Exception as e:
        logger.error(f"Retrieval failed: {e}")
        raise

    if not retrieved_docs:
        logger.warning("No relevant chunks retrieved for this question.")
        return {"answer": "I couldn't find that information in the document.", "sources": []}

    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    page_numbers = sorted(set(doc.metadata["page_number"] for doc in retrieved_docs))

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    filled_prompt = prompt.format(context=context, question=question)

    llm = get_llm()

    try:
        response = llm.invoke(filled_prompt)
    except Exception as e:
        logger.error(f"Gemini call failed: {e}")
        raise

    logger.info(f"Answer generated, based on page(s): {page_numbers}")

    return {
        "answer": response.content,
        "sources": page_numbers
    }
