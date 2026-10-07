import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.services.llm_service import ask_nutrition_assistant


query = input("Ask your nutrition question: ")

answer = ask_nutrition_assistant(query)

print("\nAI Nutrition Assistant")
print("-" * 50)
print(answer)
