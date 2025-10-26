import uuid
from django.db import models

class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DF', 'Defender'),
        ('MF', 'Midfielder'),
        ('FW', 'Forward'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=100)
    posisi = models.CharField(max_length=10, choices=POSITION_CHOICES)
    klub = models.CharField(max_length=100)
    umur = models.PositiveIntegerField()
    market_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Dalam juta Euro (€)")
    foto = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nama} - {self.posisi}"
