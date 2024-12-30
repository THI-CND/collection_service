from django.db import models

class Collection(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    recipes = models.JSONField(default=list)