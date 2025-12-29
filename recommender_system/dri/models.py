from django.db import models
from users.models import UserProfile

class DRIResult(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    bmi = models.FloatField()
    eer = models.FloatField()

    protein_min_g = models.FloatField()
    protein_max_g = models.FloatField()
    fat_min_g = models.FloatField()
    fat_max_g = models.FloatField()
    carbs_min_g = models.FloatField()
    carbs_max_g = models.FloatField()

    vitamins = models.JSONField()   # {"A": 700, "C": 90, ...}
    minerals = models.JSONField()   # {"Calcium": 1200, ...}

    created_at = models.DateTimeField(auto_now_add=True)
