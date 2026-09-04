import os
import sys

# Add the project root to sys.path so we can import 'backend' when running this script directly
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.services.llm_service import ask_nutrition_assistant


query = input("Ask your nutrition question: ")

answer = ask_nutrition_assistant(query)

print("\nAI Nutrition Assistant")
print("-" * 50)
print(answer)