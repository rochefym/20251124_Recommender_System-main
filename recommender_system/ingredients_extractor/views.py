from django.shortcuts import render
import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .extract_ingredients import extract_ingredients_from_meal


FOOD_GROUPS = {
    "Whole Grains": "全穀雜糧類",
    "Beans/Fish/Egg/Meat": "豆魚蛋肉類",
    "Vegetables": "蔬菜類",
    "Fruits": "水果類",
    "Dairy Product": "乳品類",
    "Nuts and Seeds": "堅果種子類",
    "Condiments/Seasonings": "調味品類"
}


class MealToIngredientAPIView(APIView):
    def post(self, request):
        meal_text = request.data.get("meal_text", "")

        try:
            if meal_text:
                data = extract_ingredients_from_meal(meal_text)
                
            return Response(data)

        except Exception as e:
            print("General error:", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)