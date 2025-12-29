from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import UserProfile
from .services import (
    calculate_bmi, calculate_eer,
    calculate_macros, get_micronutrient_rdas
)

class CalculateDRI(APIView):
    def post(self, request):
        data = request.data

        sex = data["sex"]
        age = data["age"]
        height_cm = data["height_cm"]
        weight_kg = data["weight_kg"]
        activity_level = data["activity_level"]

        # ---- Calculations ----
        bmi = calculate_bmi(weight_kg, height_cm)
        eer = calculate_eer(age, sex, weight_kg, height_cm, activity_level)
        protein_min_g, protein_max_g, fat_min_g, fat_max_g, carb_min_g, carb_max_g = calculate_macros(eer)
        vitamins, minerals = get_micronutrient_rdas(age, sex)

        result = {
            "bmi": bmi,
            "eer": eer,
            "protein_g": {
                "protein_min_10": protein_min_g, 
                "protein_max_35": protein_max_g
                },
            "fat_g": {
                "fat_min_20": fat_min_g, 
                "fat_max_35": fat_max_g
                },
            "carbs_g": {
                "carb_min_45": carb_min_g,
                "carb_max_65":  carb_max_g
                },
            "vitamins": vitamins,
            "minerals": minerals,
        }

        return Response(result, status=200)
