from django.db import models
from users.models import UserProfile
from menu.models import MenuItem

class IntakeRecord(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    meal = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    consumed_weight_g = models.FloatField(null=True, blank=True)
    consumed_volume_ml = models.FloatField(null=True, blank=True)

    calculated_nutrients = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
