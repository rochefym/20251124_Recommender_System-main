from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MenuItem, MenuDay, NutrientProfile
from .serializers import MenuItemSerializer, MenuDaySerializer, NutrientProfileSerializer
from django.shortcuts import get_object_or_404
import csv, io, json

class MenuItemListCreate(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class MenuItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class MenuDayList(generics.ListAPIView):
    queryset = MenuDay.objects.all()
    serializer_class = MenuDaySerializer

class MenuByDayView(APIView):
    """
    GET /api/menu/day/<int:day>/?meal_type=breakfast
    """
    def get(self, request, day_index):
        meal_type = request.query_params.get("meal_type")
        qs = MenuDay.objects.filter(day_index=day_index)
        if meal_type:
            qs = qs.filter(meal_type=meal_type)
        data = MenuDaySerializer(qs, many=True).data
        return Response(data)

class UploadMenuCSV(APIView):
    """
    POST multipart/form-data w/ file field 'file' and optional 'map_days' boolean.
    """
    def post(self, request):
        f = request.FILES.get("file")
        map_days = request.data.get("map_days", "false").lower() == "true"
        if not f:
            return Response({"detail": "file required"}, status=status.HTTP_400_BAD_REQUEST)

        # decode CSV
        try:
            content = f.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(content))
        except Exception as e:
            return Response({"detail": f"invalid csv: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        created = 0
        for row in reader:
            micron = {}
            try:
                micron = json.loads(row.get("micronutrients_json") or "{}")
            except Exception:
                micron = {}

            np, _ = NutrientProfile.objects.update_or_create(
                name=row.get("nutrient_profile_name") or row["name"],
                defaults={
                    "kcal_per_100g": float(row.get("kcal_per_100g") or 0),
                    "protein_g_per_100g": float(row.get("protein_g_per_100g") or 0),
                    "fat_g_per_100g": float(row.get("fat_g_per_100g") or 0),
                    "carbs_g_per_100g": float(row.get("carbs_g_per_100g") or 0),
                    "micronutrients": micron
                }
            )

            mi, _ = MenuItem.objects.update_or_create(
                code=row["code"],
                defaults={
                    "name": row["name"],
                    "nutrient_profile": np,
                    "default_serving_g": float(row.get("default_serving_g") or 0),
                }
            )
            created += 1

            if map_days and row.get("day_index") and row.get("meal_type"):
                from .models import MenuDay
                try:
                    MenuDay.objects.update_or_create(
                        day_index=int(row.get("day_index")),
                        meal_type=row.get("meal_type"),
                        menu_item=mi,
                        defaults={"serving_g": float(row.get("serving_g") or None)}
                    )
                except Exception:
                    pass

        return Response({"imported": created}, status=status.HTTP_200_OK)
