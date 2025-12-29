from rest_framework.views import APIView
from rest_framework.response import Response
from menu.models import MenuItem
from .services import calculate_intake

class CalculateIntake(APIView):
    def post(self, request):
        meal_id = request.data["meal_id"]
        weight = request.data.get("consumed_weight_g")
        volume = request.data.get("consumed_volume_ml")

        meal = MenuItem.objects.get(id=meal_id)
        consumed_weight_g = models.FloatField(null=True, blank=True)
        consumed_volume_ml = models.FloatField(null=True, blank=True)

        result = calculate_intake(
            meal,
            consumed_weight_g=weight,
            consumed_volume_ml=volume
        )

        return Response(result, status=200)
