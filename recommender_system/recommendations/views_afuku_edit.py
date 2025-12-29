import json
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import generate_recommendation, calculate_dri
from websockets.sync.client import connect


# Get output/response from RAG chain
class GenerateRecommendationView(APIView):
    def post(self, request):
        data = request.data

        # Validate request data is a dictionary
        if not isinstance(data, dict):
            return Response({
                "detail": "Invalid request format. Expected JSON object.",
                "received_type": type(data).__name__
            }, status=400)

        # Validate required fields
        required_fields = ["sex", "age", "height_cm", "weight_kg", "activity_level", "meal"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return Response({
                "detail": "Missing required fields",
                "missing_fields": missing_fields
            }, status=400)

        try:
            sex = data["sex"]
            age = data["age"]
            height_cm = data["height_cm"]
            weight_kg = data["weight_kg"]
            activity_level = data["activity_level"]
            dri_results = calculate_dri(sex, age, height_cm, weight_kg, activity_level)
        except (KeyError, TypeError, ValueError) as e:
            return Response({
                "detail": "Error processing patient data",
                "error": str(e)
            }, status=400)


        #MEAL
        try:
            meal_name = data["meal"].get("meal_name")
            intake_weight_g = data["meal"].get("consumed_weight_g")
        except (KeyError, AttributeError, TypeError) as e:
            return Response({
                "detail": "Error processing meal data",
                "error": str(e)
            }, status=400)
        # intake_volume_g = data["meal"].get("consumed_volume_g")


        question = (
            f"This is the patient's data: {data}. "
            f"Here is the patient's calculated DRIs: {dri_results}. "
            f"This is the patient's meal data: Meal name: {meal_name}, Consumed weight (g): {intake_weight_g}."
        )

        ws_url = getattr(settings, "RECOMMENDER_WS_URL", os.environ.get("RECOMMENDER_WS_URL", "ws://120.117.116.47:25002"))

        try:
            with connect(ws_url) as websocket:
                message = question
                websocket.send(message)
                message = websocket.recv()

                result = {
                    "dri_results": dri_results,
                    "recommendation": message
                }

            return Response(result, status=200)

        except Exception as e:
            return Response({
                "detail": "recommendation service unreachable",
                "error": str(e)
            }, status=503)


# class GenerateRecommendationView(APIView):
#     """
#     POST /api/recommendations/generate/
#     body: {"user_id": <id>, "period": "daily"/"weekly"/"monthly", "date": "YYYY-MM-DD" (optional)}
#     """
#     def post(self, request):
#         user_id = request.data.get("user_id")
#         period = request.data.get("period", "daily")
#         ref_date = request.data.get("date")

#         from users.models import UserProfile
#         try:
#             user = UserProfile.objects.get(id=user_id)
#         except UserProfile.DoesNotExist:
#             return Response({"detail": "user not found"}, status=404)

#         res = generate_recommendation(user, period=period, ref_date=None if not ref_date else ref_date)
#         return Response(res, status=200)
