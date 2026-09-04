import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.rag.retriever import search_food

load_dotenv()

# -----------------------------
# Gemini Configuration
# -----------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2
)




# -----------------------------
# RAG + LLM Function
# -----------------------------

def ask_nutrition_assistant(query: str, context_query: str = None, top_k: int = 5):

    if not query or not query.strip():
        return "Please enter a nutrition-related question."

    # Retrieve relevant food information
    search_q = context_query if context_query else query
    results = search_food(search_q, top_k=top_k)

    if not results:
        return "I could not find relevant food information."

    # Build context
    context_parts = []

    for result in results:

        payload = result.metadata if hasattr(result, "metadata") else result.payload
        if not payload and hasattr(result, "document"):
            pass

        context_parts.append(
            payload.get("text", "") if payload else result.document
        )

    context = "\n\n".join(context_parts)

    # -----------------------------
    # Prompt
    # -----------------------------

    prompt = f"""
You are an Indian food nutrition assistant.

Answer the user's question using ONLY the
nutrition information provided in the context.

Do not invent nutritional values.

If the required food information is not present
in the context, clearly say that the information
is not available.

Give simple and easy-to-understand answers.

For calorie calculations, show the calculation
when appropriate.

Nutrition Context:
------------------
{context}
------------------

User Question:
{query}

Answer:
"""

    # -----------------------------
    # Generate Response
    # -----------------------------

    response = llm.invoke(prompt)

    content = response.content
    if isinstance(content, list):
        # Extract text from the list of content blocks
        text_parts = [block.get("text", "") for block in content if isinstance(block, dict) and block.get("type") == "text"]
        return "".join(text_parts) if text_parts else str(content)
    return content