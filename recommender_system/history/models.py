from django.db import models
from users.models import UserProfile

class ActivityLog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.CharField(max_length=200)
    details = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
