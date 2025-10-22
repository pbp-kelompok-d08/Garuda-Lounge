from django.db import models
import uuid

# Create your models here.
class Match(models.Model):
    CATEGORY_CHOICES = [
        ('kualifikasi piala dunia', 'Kualifikasi Piala Dunia'),
        ('pertandingan persahabatan', 'Pertandingan Persahabatan'),
        ('piala aff', 'Piala AFF'),
        ('piala asia', 'Match'),
    ]
