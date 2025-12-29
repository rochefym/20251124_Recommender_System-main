from django.db import models
from users.models import UserProfile

class Recommendation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    period = models.CharField(max_length=20)  # daily/weekly/monthly
    suggestions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
