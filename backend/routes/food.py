from fastapi import APIRouter, HTTPException
from backend.rag.retriever import search_food

router = APIRouter(
    prefix="/api/food",
    tags=["Food Search"]
)


@router.get("/search")
def food_search(
    query: str,
    top_k: int = 5
):
    try:
        if not query.strip():
            raise HTTPException(
                status_code=400,
                detail="Food query cannot be empty."
            )

        results = search_food(
            query=query,
            top_k=top_k
        )

        foods = []

        for point in results:

            payload = point.metadata if hasattr(point, "metadata") else point.payload
            if not payload:
                payload = {}

            text = payload.get("text", "")
            
            details = {}
            for line in text.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    details[key.strip().lower()] = val.strip()

            foods.append({
                "food": payload.get("food"),
                "calories": details.get("calories", "N/A"),
                "protein": details.get("protein", "N/A"),
                "carbohydrates": details.get("carbohydrates", "N/A"),
                "fat": details.get("fat", "N/A"),
                "fibre": details.get("fibre", "N/A"),
                "score": round(point.score, 4) if hasattr(point, "score") else 0
            })

        return {
            "query": query,
            "results": foods
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )