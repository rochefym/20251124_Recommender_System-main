import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import generate_recommendation, generate_translated_recommendation, translate_text_with_ollama

class RagQueryView(APIView):

    def post(self, request):
        query = request.data.get("query")

        if not query:
            return Response(
                {"detail": "Missing 'query' in request data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            response_text = generate_recommendation(query)
            return Response(
                {"recommendation": response_text},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "detail": "Error generating recommendation.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



FOOD_INTAKE_BACKEND_URL = "https://h3vkhzth-8000.asse.devtunnels.ms/api/"

class RagQueryByPatientView(APIView):
    # ======= GET ======= 
    def get(self, request, patient_id):
        try:
            patient = requests.get(
                f"{FOOD_INTAKE_BACKEND_URL}patients/{patient_id}"
            ).json()

            intake = requests.get(
                f"{FOOD_INTAKE_BACKEND_URL}patients/{patient_id}/recommended-intake"
            ).json().get("nutritional_recommendations", {})

            meal_lines = []
            for idx, assignment in enumerate(patient.get("meal_assignments", []), start=1):
                meal_id = assignment.get("meal")
                meal = requests.get(
                    f"{FOOD_INTAKE_BACKEND_URL}meals/{meal_id}"
                ).json()

                meal_lines.append(
                    f"Meal {idx}: {meal.get('meal_name', 'N/A')}"
                )

            query = f"""
PATIENT DETAILS:
Patient Name: {patient.get('name')}
Age: {patient.get('age')}
Gender: {patient.get('sex').capitalize()}
Height: {patient.get('height_cm')} cm
Weight: {patient.get('weight_kg')} kg
BMI: {patient.get('bmi')}
Heart Rate: {patient.get('heart_rate')} bpm
Blood Pressure: {patient.get('systolic_bp')}/{patient.get('diastolic_bp')} mmHg
Activity Level: {patient.get('activity_level').capitalize()}

RECOMMENDED DAILY INTAKE:
Calories: {intake.get('daily_caloric_needs')} kcal
Protein: {intake.get('protein')} g
Carbohydrates: {intake.get('carbohydrate')} g
Fat: {intake.get('fat')} g
Total Fiber: {intake.get('total_fiber')} g
Alpha Linolenic Acid: {intake.get('alpha_linolenic_acid')} g
Linoleic Acid: {intake.get('linoleic_acid')} g
Total Water: {intake.get('total_water')} L

MEAL INTAKES:
""" + "\n".join(meal_lines)

            return Response(
                {"recommendation": generate_recommendation(query)},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"detail": "Error generating recommendation", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

    # ======= POST =========
    def post(self, request, patient_id):
        try:
            patient = requests.get(
                f"{FOOD_INTAKE_BACKEND_URL}patients/{patient_id}"
            ).json()

            intake = requests.get(
                f"{FOOD_INTAKE_BACKEND_URL}patients/{patient_id}/recommended-intake"
            ).json().get("nutritional_recommendations", {})

            meal_lines = []
            for idx, assignment in enumerate(patient.get("meal_assignments", []), start=1):
                meal_id = assignment.get("meal")
                meal = requests.get(
                    f"{FOOD_INTAKE_BACKEND_URL}meals/{meal_id}"
                ).json()

                meal_lines.append(
                    f"Meal {idx}: {meal.get('meal_name', 'N/A')}"
                )

            query = f"""
PATIENT DETAILS:
Patient Name: {patient.get('name')}
Age: {patient.get('age')}
Gender: {patient.get('sex').capitalize()}
Height: {patient.get('height_cm')} cm
Weight: {patient.get('weight_kg')} kg
BMI: {patient.get('bmi')}
Heart Rate: {patient.get('heart_rate')} bpm
Blood Pressure: {patient.get('systolic_bp')}/{patient.get('diastolic_bp')} mmHg
Activity Level: {patient.get('activity_level').capitalize()}

RECOMMENDED DAILY INTAKE:
Calories: {intake.get('daily_caloric_needs')} kcal
Protein: {intake.get('protein')} g
Carbohydrates: {intake.get('carbohydrate')} g
Fat: {intake.get('fat')} g
Total Fiber: {intake.get('total_fiber')} g
Alpha Linolenic Acid: {intake.get('alpha_linolenic_acid')} g
Linoleic Acid: {intake.get('linoleic_acid')} g
Total Water: {intake.get('total_water')} L

MEAL INTAKES:
""" + "\n".join(meal_lines)

            return Response(
                {"recommendation": generate_recommendation(query)},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"detail": "Error generating recommendation", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



# ======= VIEWS FOR CHINESE TRANSLATION =======

class RagQueryChineseView(APIView):

    def post(self, request):
        query = request.data.get("query")

        if not query:
            return Response(
                {"detail": "Missing 'query' in request data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            response_text = generate_translated_recommendation(query)
            return Response(
                {"recommendation": response_text},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "detail": "Error generating recommendation.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class RagQueryInChineseByPatientView(APIView):
    # ======= GET ======= 
    def get(self, request, patient_id):
        try:
            patient = requests.get(
                f"{FOOD_INTAKE_BACKEND_URL}patients/{patient_id}"
            ).json()

            intake = requests.get(
                f"{FOOD_INTAKE_BACKEND_URL}patients/{patient_id}/recommended-intake"
            ).json().get("nutritional_recommendations", {})

            meal_lines = []
            for idx, assignment in enumerate(patient.get("meal_assignments", []), start=1):
                meal_id = assignment.get("meal")
                meal = requests.get(
                    f"{FOOD_INTAKE_BACKEND_URL}meals/{meal_id}"
                ).json()

                meal_lines.append(
                    f"Meal {idx}: {meal.get('meal_name', 'N/A')}"
                )

            query = f"""
PATIENT DETAILS:
Patient Name: {patient.get('name')}
Age: {patient.get('age')}
Gender: {patient.get('sex').capitalize()}
Height: {patient.get('height_cm')} cm
Weight: {patient.get('weight_kg')} kg
BMI: {patient.get('bmi')}
Heart Rate: {patient.get('heart_rate')} bpm
Blood Pressure: {patient.get('systolic_bp')}/{patient.get('diastolic_bp')} mmHg
Activity Level: {patient.get('activity_level').capitalize()}

RECOMMENDED DAILY INTAKE:
Calories: {intake.get('daily_caloric_needs')} kcal
Protein: {intake.get('protein')} g
Carbohydrates: {intake.get('carbohydrate')} g
Fat: {intake.get('fat')} g
Total Fiber: {intake.get('total_fiber')} g
Alpha Linolenic Acid: {intake.get('alpha_linolenic_acid')} g
Linoleic Acid: {intake.get('linoleic_acid')} g
Total Water: {intake.get('total_water')} L

MEAL INTAKES:
""" + "\n".join(meal_lines)

            return Response(
                {"recommendation": generate_translated_recommendation(query)},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"detail": "Error generating recommendation", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

    # ======= POST =========
    def post(self, request, patient_id):
        try:
            patient = requests.get(
                f"{FOOD_INTAKE_BACKEND_URL}patients/{patient_id}"
            ).json()

            intake = requests.get(
                f"{FOOD_INTAKE_BACKEND_URL}patients/{patient_id}/recommended-intake"
            ).json().get("nutritional_recommendations", {})

            meal_lines = []
            for idx, assignment in enumerate(patient.get("meal_assignments", []), start=1):
                meal_id = assignment.get("meal")
                meal = requests.get(
                    f"{FOOD_INTAKE_BACKEND_URL}meals/{meal_id}"
                ).json()

                meal_lines.append(
                    f"Meal {idx}: {meal.get('meal_name', 'N/A')}"
                )

            query = f"""
PATIENT DETAILS:
Patient Name: {patient.get('name')}
Age: {patient.get('age')}
Gender: {patient.get('sex').capitalize()}
Height: {patient.get('height_cm')} cm
Weight: {patient.get('weight_kg')} kg
BMI: {patient.get('bmi')}
Heart Rate: {patient.get('heart_rate')} bpm
Blood Pressure: {patient.get('systolic_bp')}/{patient.get('diastolic_bp')} mmHg
Activity Level: {patient.get('activity_level').capitalize()}

RECOMMENDED DAILY INTAKE:
Calories: {intake.get('daily_caloric_needs')} kcal
Protein: {intake.get('protein')} g
Carbohydrates: {intake.get('carbohydrate')} g
Fat: {intake.get('fat')} g
Total Fiber: {intake.get('total_fiber')} g
Alpha Linolenic Acid: {intake.get('alpha_linolenic_acid')} g
Linoleic Acid: {intake.get('linoleic_acid')} g
Total Water: {intake.get('total_water')} L

MEAL INTAKES:
""" + "\n".join(meal_lines)

            return Response(
                {"recommendation": generate_translated_recommendation(query)},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"detail": "Error generating recommendation", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )