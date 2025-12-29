from django.db import models

class SourceDocument(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    embedding = models.BinaryField()  # vector stored raw
    source = models.CharField(max_length=100)  # NIH / NASEM
