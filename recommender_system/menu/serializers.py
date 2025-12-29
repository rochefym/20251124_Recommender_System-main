from rest_framework import serializers
from .models import NutrientProfile, MenuItem, MenuDay

class NutrientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutrientProfile
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    nutrient_profile = NutrientProfileSerializer()
    class Meta:
        model = MenuItem
        fields = '__all__'

class MenuDaySerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer()
    class Meta:
        model = MenuDay
        fields = '__all__'
