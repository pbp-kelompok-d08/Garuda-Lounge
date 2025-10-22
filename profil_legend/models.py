import uuid
from django.db import models
from django.contrib.auth.models import User

class LegendPlayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    current_club = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(default=0)
    market_value = models.CharField(max_length=50, blank=True)
    photo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name