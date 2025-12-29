# menu/models.py
from django.db import models

class NutrientProfile(models.Model):
    """
    Canonical nutrient profile for a single ingredient or assembled food.
    Values are per 100 grams.
    """
    name = models.CharField(max_length=255, unique=True)
    kcal_per_100g = models.FloatField(default=0.0)
    protein_g_per_100g = models.FloatField(default=0.0)
    fat_g_per_100g = models.FloatField(default=0.0)
    carbs_g_per_100g = models.FloatField(default=0.0)

    # store micronutrients as dict; keys should be consistent (e.g. "Vitamin C (mg)")
    micronutrients = models.JSONField(default=dict, blank=True)

    density_g_per_ml = models.FloatField(null=True, blank=True, help_text="optional; g per ml")

    def nutrients_for_grams(self, grams: float) -> dict:
        scale = grams / 100.0
        out = {
            "kcal": round(self.kcal_per_100g * scale, 2),
            "protein_g": round(self.protein_g_per_100g * scale, 2),
            "fat_g": round(self.fat_g_per_100g * scale, 2),
            "carbs_g": round(self.carbs_g_per_100g * scale, 2)
        }
        # micronutrients: multiply each
        for k, v in (self.micronutrients or {}).items():
            out[k] = round(v * scale, 3)
        return out

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    A served menu entry in the 14-day cycle.
    default_serving_g is the plated portion weight (grams).
    If a dish is a soup stored by volume, set density_g_per_ml on NutrientProfile instead.
    """
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=255)
    nutrient_profile = models.ForeignKey(NutrientProfile, on_delete=models.PROTECT)
    default_serving_g = models.FloatField(null=True, blank=True, help_text="grams")
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def nutrients_for_serving(self, grams: float = None) -> dict:
        grams = grams if grams is not None else self.default_serving_g or 100.0
        return self.nutrient_profile.nutrients_for_grams(grams)

    def __str__(self):
        return f"{self.code} — {self.name}"


class MenuDay(models.Model):
    """
    Links a day index (1–14) to multiple menu items and a meal_type.
    This allows multiple menu items per meal (e.g., congee + side veg).
    """
    DAY_CHOICES = [(i, f"Day {i}") for i in range(1, 15)]
    MEAL_TYPES = (
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
    )
    day_index = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    # default portion for this menu mapping (grams); may override MenuItem.default_serving_g
    serving_g = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ("day_index", "meal_type", "menu_item")

    def serving_grams(self):
        return self.serving_g if self.serving_g is not None else (self.menu_item.default_serving_g or 100.0)

    def nutrients_for_serving(self):
        return self.menu_item.nutrients_for_serving(self.serving_grams())

    def __str__(self):
        return f"Day {self.day_index} - {self.meal_type} - {self.menu_item.code}"
