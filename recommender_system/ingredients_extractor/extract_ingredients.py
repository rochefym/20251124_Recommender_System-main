import os
import json
import re
from rest_framework.response import Response
import requests
import time

# Load local LLM model from Ollama server
# LLM Model: deepseek-r1:8b
OLLAMA_URL = "http://localhost:11434/api/generate"

def extract_ingredients_from_meal(meal_text: str):
    # Create detailed prompt for ingredient extraction
    prompt = f"""
    You are a professional nutrition expert. Analyze the meal: "{meal_text}" and extract ALL individual ingredients.

    For each ingredient, provide:
    1. "name": The exact ingredient name (no cooking methods, no descriptors)
    2. "food_group": Choose ONLY from these 7 categories:
    - "全穀雜糧類" (Whole Grains: rice, bread, pasta, quinoa, oats)
    - "豆魚蛋肉類" (Beans/Fish/Egg/Meat: tofu, chicken, beef, fish, beans, eggs)
    - "蔬菜類" (Vegetables: all vegetables including leafy greens, root vegetables)
    - "水果類" (Fruits: all fresh and dried fruits)
    - "乳品類" (Dairy Product: milk, cheese, yogurt, butter)
    - "堅果種子類" (Nuts and Seeds: almonds, peanuts, sesame seeds)
    - "調味品類" (Condiments/Seasonings: soy sauce, salt, sugar, oil, vinegar, spices, herbs)

    3. "nutrients": Choose from these 5 nutrients based on what the ingredient naturally contains:
    - "Carbohydrate" (grains, fruits, some vegetables)
    - "Protein" (meat, fish, beans, eggs, dairy)
    - "Fats" (oils, nuts, meat, dairy)
    - "Water" (vegetables, fruits)
    - "Total Fiber" (vegetables, fruits, whole grains)

    IMPORTANT RULES:
    - Break down complex dishes into individual components
    - Condiments like soy sauce, vinegar, oil are "調味品類"
    - If an ingredient has no significant nutrients, use empty array []
    - Use standardized ingredient names (e.g., "scallion" not "green onion")
    - Do NOT include cooking methods as ingredients
    - Do NOT invent new food groups; only use the 7 listed above
    - Use english names for ingredients and nutrients

    Return ONLY valid JSON in this exact format:
    {{
        "ingredients": [
            {{
                "name": "ingredient_name",
                "food_group": "category",
                "nutrients": ["nutrient1", "nutrient2"]
            }}
        ]
    }}
    """
   
    try:
        # Ollama API call
        raw_output = get_ollama_response(prompt)["response"]

        # Clean and extract JSON from the response
        if raw_output:
            # Try to find JSON pattern in the response
            json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                # Parse JSON to validate it
                parsed_json = json.loads(json_str)
                return parsed_json
            else:
                # Fallback: return empty ingredients if no JSON found
                return {"ingredients": []}
        else:
            return {"ingredients": []}
           
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Raw response: {raw_output}")
        return {"ingredients": []}
    except Exception as e:
        print(f"Error calling Ollama API: {e}")
        return {"ingredients": []}
    

# Ollama 
def get_ollama_response(prompt):
    payload = {
            "model": "deepseek-r1:8b",
            "prompt": prompt,
            "stream": False
    }

    try:
        start = time.time()  # start timer
        ollama_response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=30
        )
        ollama_response.raise_for_status()

        latency_ms = (time.time() - start) * 1000  # convert to milliseconds
        print(f"\nLatency: {latency_ms:.2f} ms\n")

        data = ollama_response.json()
        return data
    except Exception:
        return Exception


# print (extract_ingredients_from_meal("Stir-fried chicken with broccoli and garlic sauce"))
