from django.forms import ModelForm
from match.models import Pertandingan

class PertandinganForm(ModelForm):
    class Meta:
        model = Pertandingan
        fields = [
            "jenis_pertandingan",
            "tim_tuan_rumah",
            "tim_tamu",
            "bendera_tuan_rumah",
            "bendera_tamu",
            "tanggal",
            "stadion",
            "skor_tuan_rumah",
            "skor_tamu",
            "pencetak_gol_tuan_rumah",
            "pencetak_gol_tamu",
            "starter_tuan_rumah",
            "starter_tamu",
            "pengganti_tuan_rumah",
            "pengganti_tamu",
            "manajer_tuan_rumah",
            "manajer_tamu",
            "highlight",
            "penguasaan_bola_tuan_rumah",
            "penguasaan_bola_tamu",
            "tembakan_tuan_rumah",
            "tembakan_tamu",
            "on_target_tuan_rumah",
            "on_target_tamu",
            "akurasi_umpan_tuan_rumah",
            "akurasi_umpan_tamu",
            "pelanggaran_tuan_rumah",
            "pelanggaran_tamu",
            "kartu_kuning_tuan_rumah",
            "kartu_kuning_tamu",
            "kartu_merah_tuan_rumah",
            "kartu_merah_tamu",
            "offside_tuan_rumah",
            "offside_tamu",
            "corner_tuan_rumah",
            "corner_tamu",
        ]