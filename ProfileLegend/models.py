import uuid
from django.db import models

class LegendPlayer(models.Model):
    class Position(models.TextChoices):
        KIPER = "Kiper", "Kiper"
        BEK = "Bek", "Bek"
        GELANDANG = "Gelandang", "Gelandang"
        PENYERANG = "Penyerang", "Penyerang"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=20, choices=Position.choices)
    is_legend = models.BooleanField(default=True)
    club = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.position})"
