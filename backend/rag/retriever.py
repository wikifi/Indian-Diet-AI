import os
import shutil

original_symlink = getattr(os, "symlink", None)
def symlink_wrapper(src, dst, *args, **kwargs):
    if not os.path.isabs(src):
        src = os.path.join(os.path.dirname(dst), src)
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
os.symlink = symlink_wrapper

from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

# -----------------------------
# Configuration
# -----------------------------

COLLECTION_NAME = "indian_foods"

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# -----------------------------
# Qdrant Client
# -----------------------------

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    check_compatibility=False,
    timeout=60
)

client.set_model("sentence-transformers/all-MiniLM-L6-v2")
client.set_sparse_model("prithivida/Splade_PP_en_v1")


def search_food(query: str, top_k: int = 5):
    """
    Search Indian food information from Qdrant.
    """

    results = client.query(
        collection_name=COLLECTION_NAME,
        query_text=query,
        limit=top_k
    )

    return results


# -----------------------------
# Test Retriever
# -----------------------------

if __name__ == "__main__":

    query = input("Enter your food query: ")

    results = search_food(query)

    print("\nSearch Results\n")

    for result in results:

        print("-" * 50)

        payload = result.metadata if hasattr(result, "metadata") else result.payload
        if not payload and hasattr(result, "document"):
            # sometimes Qdrant QueryResponse holds document and metadata separately
            pass

        print("Food:", payload.get("food") if payload else result.document)
        print("Category:", payload.get("category") if payload else "N/A")
        print("Serving:", payload.get("serving") if payload else "N/A")

        print("Information:")
        print(payload.get("text") if payload else result.document)

        print("Similarity Score:", result.score)