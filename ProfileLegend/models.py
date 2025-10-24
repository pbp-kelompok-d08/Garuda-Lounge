import uuid
from django.db import models
from django.contrib.auth.models import User

class LegendPlayer(models.Model):
    POSITION_CHOICES = [
        ('Kiper', 'Kiper'),
        ('Bek', 'Bek'),
        ('Gelandang', 'Gelandang'),
        ('Penyerang', 'Penyerang'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    is_legend = models.BooleanField(default=True)
    club = models.CharField(max_length=100, blank=True)
    age = models.CharField(max_length=50, blank=True)
    photo_url = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Legend Player"
        verbose_name_plural = "Legend Players"
    
    def __str__(self):
        return self.name
