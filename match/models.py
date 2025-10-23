from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
# Tim nasional yang bertanding
class Tim(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=100, unique=True) # Contoh: Indonesia, Irak
    logo_url = models.URLField(max_length=500, blank=True, null=True)
    rank_fifa =  models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Tim Nasional"

    def __str__(self):
        return self.nama

# Pemain Nasional (yang bertanding ataupun tidak)
class Pemain(models.Model):
    POSISI_CHOICES = [
        ('GK', 'Kiper'), ('DF', 'Bek'), ('MF', 'Gelandang'), ('FW', 'Penyerang'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField("Nama", max_length=100)
    posisi = models.CharField("Posisi", max_length=2, choices=POSISI_CHOICES, blank=True, null=True)
    is_pemain_legend = models.BooleanField(default=False)
    nama_klub = models.CharField("Nama Klub", max_length=100, blank=True, null=True)
    umur = models.PositiveIntegerField("Umur", blank=True, null=True)
    market_value = models.CharField("Market Value", max_length=50, blank=True, null=True)
    foto_url = models.URLField("Foto Profil", max_length=500, blank=True, null=True)
    tahun_bermain = models.CharField("Rentang Timnas", max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Pemain"
        ordering = ['nama']

    def __str__(self):
        posisi_display = self.get_posisi_display() or 'N/A'
        return f"{self.nama} ({posisi_display})"

# Pertandingan Internasional
class Pertandingan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    JENIS_PERTANDINGAN_CHOICES = [
        ('kualifikasi piala dunia', 'Kualifikasi Piala Dunia'), 
        ('pertandingan persahabatan', 'Pertandingan Persahabatan'), 
        ('piala asean', 'Piala ASEAN'), 
        ('piala asia', 'Piala Asia'),
    ]
    jenis_pertandingan = models.CharField("Jenis Pertandingan", max_length=100, choices=JENIS_PERTANDINGAN_CHOICES, blank=True, null=True)

    # Merujuk ke tim nasional
    tim_tuan_rumah = models.ForeignKey(Tim, on_delete=models.CASCADE, related_name="laga_kandang")
    tim_tamu = models.ForeignKey(Tim, on_delete=models.CASCADE, related_name="laga_tandang")

    tanggal_waktu = models.DateTimeField(default=timezone.now)
    stadion = models.CharField(max_length=100, blank=True, null=True)

    skor_tuan_rumah = models.PositiveIntegerField(blank=True, null=True)
    skor_tamu = models.PositiveIntegerField(blank=True, null=True)

    pencetak_gol_tuan_rumah = models.TextField(blank=True, null=True)
    pencetak_gol_tamu = models.TextField(blank=True, null=True)

    kartu_merah_tuan_rumah_str = models.TextField(blank=True, null=True)
    kartu_merah_tamu_str = models.TextField(blank=True, null=True)
    kartu_kuning_tuan_rumah_str = models.TextField(blank=True, null=True)
    kartu_kuning_tamu_str = models.TextField(blank=True, null=True)

    pemain_bermain = models.ManyToManyField(
        Pemain,
        through='DetailPemainLaga', # Menunjuk ke model perantara
        related_name="laga_dimainkan",
        blank=True # Boleh kosong jika lineup belum dimasukkan
    )
    
    manajer_tuan_rumah_nama = models.CharField("Nama Manajer Tuan Rumah", max_length=100, blank=True, null=True)
    manajer_tamu_nama = models.CharField("Nama Manajer Tamu", max_length=100, blank=True, null=True)
    highlight_url = models.URLField("Highlight", max_length=500, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Pertandingan Internasional"
        ordering = ['-tanggal_waktu']

    def __str__(self):
        return f"{self.tim_tuan_rumah} vs {self.tim_tamu} ({self.tanggal_waktu.date()})"
    
# Model perantara yang menghubungkan Pertandingan dan Pemain
class DetailPemainLaga(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    pertandingan = models.ForeignKey(
        Pertandingan,
        on_delete=models.CASCADE,
        related_name="detail_pemain" # Cara akses: laga.detail_pemain.all()
    )
    pemain = models.ForeignKey(
        Pemain,
        on_delete=models.CASCADE,
        related_name="detail_laga" # Cara akses: pemain.detail_laga.all()
    )
    # Timnas mana yang dibela pemain saat laga ini
    tim = models.ForeignKey(
        Tim,
        on_delete=models.CASCADE
    )

    # Membedakan pemain starter dan cadangan
    is_starter = models.BooleanField(
        default=False,
        help_text="Centang jika pemain ini adalah bagian dari Starting XI"
    )

    class Meta:
        # memastikan tidak ada pemain yang duplikat
        unique_together = ('pertandingan', 'pemain')
        verbose_name_plural = "Detail Pemain Per Laga"
        ordering = ['pertandingan', 'tim', '-is_starter', 'pemain__nama'] # Urutan logikanya

    def __str__(self):
        status = "Starter" if self.is_starter else "Cadangan"
        return f"{self.pemain.nama} ({status}) - {self.pertandingan}"