import uuid
from django.db import models

class Merch(models.Model):
    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('shoes', 'Shoes'),
        ('gk gloves', 'GK Gloves'),
        ('ball', 'Ball'),
        ('jacket', 'Jacket'),
        ('scarf', 'Scarf'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='jersey')
    price = models.IntegerField()
    thumbnail = models.URLField()
    product_link = models.URLField()
    
    def __str__(self):
        return self.name