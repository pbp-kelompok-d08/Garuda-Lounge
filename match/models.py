from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class Pertandingan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    JENIS_PERTANDINGAN_CHOICES = [
        ('kualifikasi piala dunia', 'Kualifikasi Piala Dunia'), 
        ('pertandingan persahabatan', 'Pertandingan Persahabatan'), 
        ('piala asean', 'Piala ASEAN'), 
        ('piala asia', 'Piala Asia'),
    ]
    # Header
    jenis_pertandingan = models.CharField("Jenis Pertandingan", max_length=100, choices=JENIS_PERTANDINGAN_CHOICES, blank=True, null=True)

    tim_tuan_rumah = models.CharField(max_length=100, blank=True, null=True)
    tim_tamu = models.CharField(max_length=100, blank=True, null=True)

    bendera_tuan_rumah = models.URLField("Bendera Tuan Rumah", max_length=500, blank=True, null=True)
    bendera_tamu = models.URLField("Bendera Tamu", max_length=500, blank=True, null=True)

    tanggal = models.CharField(max_length=100, blank=True, null=True)
    stadion = models.CharField(max_length=100, blank=True, null=True) # Ditampilkan paling akhir

    skor_tuan_rumah = models.PositiveIntegerField(blank=True, null=True)
    skor_tamu = models.PositiveIntegerField(blank=True, null=True)

    pencetak_gol_tuan_rumah = models.TextField(blank=True, null=True)
    pencetak_gol_tamu = models.TextField(blank=True, null=True)

    # Susunan tim
    starter_tuan_rumah = models.TextField(blank=True, null=True)
    starter_tamu = models.TextField(blank=True, null=True)

    pengganti_tuan_rumah = models.TextField(blank=True, null=True)
    pengganti_tamu = models.TextField(blank=True, null=True)
    
    manajer_tuan_rumah= models.CharField("Nama Manajer Tuan Rumah", max_length=100, blank=True, null=True)
    manajer_tamu = models.CharField("Nama Manajer Tamu", max_length=100, blank=True, null=True)
    
    highlight = models.URLField("Highlight", max_length=500, blank=True, null=True)

    # Statistik 
    penguasaan_bola_tuan_rumah = models.PositiveIntegerField(blank=True, null=True)
    penguasaan_bola_tamu = models.PositiveIntegerField(blank=True, null=True)

    tembakan_tuan_rumah = models.PositiveIntegerField(blank=True, null=True)
    tembakan_tamu = models.PositiveIntegerField(blank=True, null=True)

    on_target_tuan_rumah = models.PositiveIntegerField(blank=True, null=True) # Maksudnya tembakan ke arah gawang
    on_target_tamu = models.PositiveIntegerField(blank=True, null=True)
    
    akurasi_umpan_tuan_rumah = models.PositiveIntegerField(blank=True, null=True)
    akurasi_umpan_tamu = models.PositiveIntegerField(blank=True, null=True)

    pelanggaran_tuan_rumah = models.PositiveIntegerField(blank=True, null=True)
    pelanggaran_tamu = models.PositiveIntegerField(blank=True, null=True)

    kartu_kuning_tuan_rumah = models.PositiveIntegerField(blank=True, null=True)
    kartu_kuning_tamu = models.PositiveIntegerField(blank=True, null=True)

    kartu_merah_tuan_rumah = models.PositiveIntegerField(blank=True, null=True)
    kartu_merah_tamu = models.PositiveIntegerField(blank=True, null=True)

    offside_tuan_rumah = models.PositiveIntegerField(blank=True, null=True)
    offside_tamu = models.PositiveIntegerField(blank=True, null=True)

    corner_tuan_rumah = models.PositiveIntegerField(blank=True, null=True)
    corner_tamu = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Pertandingan Internasional"
        ordering = ['-tanggal']

    def __str__(self):
        return f"{self.tim_tuan_rumah} vs {self.tim_tamu} ({self.tanggal})"