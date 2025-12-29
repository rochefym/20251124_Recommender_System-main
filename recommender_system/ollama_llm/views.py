from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
import requests

# Load local LLM model from Ollama server
# LLM Model: deepseek-r1:8b
OLLAMA_URL = "http://localhost:11434/api/generate"


class GetOllamaLLMResponseView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt")

        if not prompt:
            return Response(
                {"error": "Prompt is required."},
                status=400
            )

        payload = {
            "model": "deepseek-r1:8b",
            "prompt": prompt,
            "stream": False
        }

        try:
            ollama_response = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=30
            )
            ollama_response.raise_for_status()

            data = ollama_response.json()
            llm_output = data.get("response", "")

            return Response({"response": llm_output})

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": str(e)},
                status=500
            )
        


        
