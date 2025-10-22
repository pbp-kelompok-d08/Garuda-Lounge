from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
# # class Match(models.Model):
#     CATEGORY_CHOICES = [
#         ('kualifikasi piala dunia', 'Kualifikasi Piala Dunia'),
#         ('pertandingan persahabatan', 'Pertandingan Persahabatan'),
#         ('piala aff', 'Piala AFF'),
#         ('piala asia', 'Match'),
#     ]

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


# Menyimpan data semua manajer
class Manajer(models.Model):
    nama = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Manajer"

    def __str__(self):
        return self.nama

# Menyimpan data semua pemain
class Pemain(models.Model):
    POSISI_CHOICES = [
        ('GK', 'Kiper'),
        ('DF', 'Bek'),
        ('MF', 'Gelandang'),
        ('FW', 'Penyerang'),
    ]

    nama = models.CharField(max_length=100)
    posisi = models.CharField(max_length=2, choices=POSISI_CHOICES, blank=True, null=True)
    umur = models.PositiveIntegerField(blank=True, null=True)
    foto_url = models.URLField(max_length=500, blank=True, null=True)
    is_pemain_legend = models.BooleanField(default=False)
    tahun_bermain = models.CharField(max_length=100) # rentang waktu pemain tsb bermain di timnas 

    class Meta:
        verbose_name_plural = "Pemain"

    def __str__(self):
        return f"{self.nama} ({self.get_posisi_display() or 'N/A'})"


# Menyimpan data klub, termasuk roster pemain dan staf manajer.
class Tim(models.Model):
    nama = models.CharField(max_length=100, unique=True)

    # Roster staf manajer
    staf_manajer = models.ManyToManyField(
        Manajer, 
        related_name="tim_dilatih",
        blank=True
    )
    
    # Roster pemain
    daftar_pemain = models.ManyToManyField(
        Pemain, 
        related_name="tim_dibela",
        blank=True
    )

    class Meta:
        verbose_name_plural = "Tim"

    def __str__(self):
        return self.nama

# Menyimpan data semua pertandingan (ini model utamanya)
class Pertandingan(models.Model):
    """Model event utama yang mengikat 2 tim, skor, dan data laga."""
    CATEGORY_CHOICES = [
        ('kualifikasi piala dunia', 'Kualifikasi Piala Dunia'),
        ('pertandingan persahabatan', 'Pertandingan Persahabatan'),
        ('piala aff', 'Piala AFF'),
        ('piala asia', 'Piala Asia'),
    ]

    tanggal_waktu = models.DateTimeField(default=timezone.now)
    stadion = models.CharField(max_length=100, blank=True, null=True)

    tim_tuan_rumah = models.ForeignKey(
        Tim, 
        on_delete=models.CASCADE, 
        related_name="laga_kandang"
    )
    tim_tamu = models.ForeignKey(
        Tim, 
        on_delete=models.CASCADE, 
        related_name="laga_tandang"
    )

    # Hasil akhir (bisa null jika laga belum selesai)
    skor_tuan_rumah = models.PositiveIntegerField(blank=True, null=True)
    skor_tamu = models.PositiveIntegerField(blank=True, null=True)

    # Ini adalah "link" yang memberi tahu Django untuk menggunakan model 'DetailPemainLaga' sebagai perantara.
    pemain_bermain = models.ManyToManyField(
        Pemain,
        through='DetailPemainLaga',
        related_name="laga_dimainkan",
        blank=True
    )

    class Meta:
        verbose_name_plural = "Pertandingan"
        ordering = ['-tanggal_waktu'] # Menampilkan laga terbaru di atas

    def __str__(self):
        return f"{self.tim_tuan_rumah} vs {self.tim_tamu} ({self.tanggal_waktu.date()})"

# Statistik setiap tim dalam suatu pertandingan
class StatistikTimPertandingan(models.Model):
    """Menyimpan statistik agregat (total) per tim di satu laga."""
    pertandingan = models.ForeignKey(
        Pertandingan, 
        on_delete=models.CASCADE, 
        related_name="statistik_tim" # Akses: laga.statistik_tim.all()
    )
    tim = models.ForeignKey(
        Tim, 
        on_delete=models.CASCADE, 
        related_name="statistik_laga"
    )

    # Contoh statistik
    tembakan = models.PositiveIntegerField(default=0)
    tembakan_ke_gawang = models.PositiveIntegerField(default=0)
    penguasaan_bola = models.PositiveIntegerField(default=0, help_text="Persentase, misal: 55")
    pelanggaran = models.PositiveIntegerField(default=0)
    kartu_kuning = models.PositiveIntegerField(default=0)
    kartu_merah = models.PositiveIntegerField(default=0)
    offside = models.PositiveIntegerField(default=0)
    tendangan_sudut = models.PositiveIntegerField(default=0)

    class Meta:
        # Satu tim hanya boleh punya satu set statistik per laga
        unique_together = ('pertandingan', 'tim')
        verbose_name_plural = "Statistik Tim Pertandingan"

    def __str__(self):
        return f"Statistik {self.tim.nama} di laga {self.pertandingan}"

# Detail pemain starter, cadangan, dan siapa mengganti siapa
class DetailPemainLaga(models.Model):
    """
    Model perantara (through model) yang menghubungkan Pertandingan dan Pemain.
    Di sinilah kita menyimpan status STARTER vs CADANGAN.
    """
    pertandingan = models.ForeignKey(
        Pertandingan, 
        on_delete=models.CASCADE,
        related_name="detail_pemain" # Akses: laga.detail_pemain.all()
    )
    pemain = models.ForeignKey(
        Pemain, 
        on_delete=models.CASCADE,
        related_name="detail_laga" # Akses: pemain.detail_laga.all()
    )
    # Tim mana yang dibela pemain SAAT LAGA INI
    tim = models.ForeignKey(
        Tim, 
        on_delete=models.CASCADE
    )

    # --- Ini adalah jawaban untuk Starter vs Cadangan ---
    is_starter = models.BooleanField(
        default=False, 
        help_text="Centang jika pemain ini adalah bagian dari Starting XI"
    )

    class Meta:
        # Satu pemain tidak bisa ada dua kali di satu laga
        unique_together = ('pertandingan', 'pemain')
        verbose_name_plural = "Detail Pemain Per Laga"

    def __str__(self):
        status = "Starter" if self.is_starter else "Cadangan"
        return f"{self.pemain.nama} ({status}) - {self.pertandingan}"
