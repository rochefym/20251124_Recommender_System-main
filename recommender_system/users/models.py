from django.db import models

class UserProfile(models.Model):
    SEX_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    age = models.IntegerField()
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    activity_level = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
