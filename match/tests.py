from django.test import TestCase, Client

from match.forms import PertandinganForm
from .models import Pertandingan
from django.urls import reverse
import uuid
import datetime

class MatchTest(TestCase):
    def test_match_url_is_exist(self):
        response = Client().get('/match/')
        self.assertEqual(response.status_code, 200)

    def test_match_using_match_template(self):
        response = Client().get('/match/')
        self.assertTemplateUsed(response, 'match.html')

    def test_nonexistent_page(self):
        response = Client().get('/burhan_always_exists/')
        self.assertEqual(response.status_code, 404)

    def test_pertandingan_creation(self):
        pertandingan = Pertandingan.objects.create(
            jenis_pertandingan="kualifikasi piala dunia",
            tim_tuan_rumah="Irak",
            tim_tamu="Indonesia",
            bendera_tuan_rumah="https://ssl.gstatic.com/onebox/media/sports/logos/kErkaIWGPh_VGrd4T6NwUA_96x96.png",
            bendera_tamu="https://ssl.gstatic.com/onebox/media/sports/logos/S5ivsscrfCG1mgqceKMPlQ_96x96.png",
            tanggal="12/10/2025",
            stadion="King Abdullah Sports City",
            skor_tuan_rumah=1,
            skor_tamu=0,
            pencetak_gol_tuan_rumah="Zidane Iqbal 76'",
            pencetak_gol_tamu="", # coba ini
            starter_tuan_rumah="Jalal Hasan;Hussein Ali;Zaid Tahseen;Merchas Doski;Manaf Younis;Bashar Resan;Amir Al-Ammari;Kevin Yakob;Ibrahim Bayesh;Mohamed Ali;Sherko Karim Gubari",
            starter_tamu="Maarten Paes;Dean James;Jay Idzes;Kevin Diks;Rizky Ridho;Thom Haye;Calvin Verdonk;Joey Pelupessy; Ricky Kambuaya;Eliano Reijnders;Mauro Ziljstra",
            pengganti_tuan_rumah="Rebin Sulaka;Youssef Amyn;Zidane Iqbal;Ali jAsim;Amar Muhsin;Fahad Talib;Akam Hashim;Hasan Abdulkareem;Ahmed Al-Hajjaj;Aimar Sher;Mustafa Saadoon;Ahmed Basil",
            pengganti_tamu="Ramadhan Sananta;Miliano Jonathans;Ole Romeny;Ragnar Oratmangoen;Nathan Tjoe-A-On;Jordi Amat;Sandy Walsh;Stefano Lilipaly;Ernando Ari Sutaryadi;Nadeo Argawinata;Marc klok;Shayne Pattynama",
            manajer_tuan_rumah="Graham Arnold",
            manajer_tamu="Patrick Kluivert",
            highlight="youtube.com/watch?v=YLPOfyDxYXg&feature=onebox",
            penguasaan_bola_tuan_rumah=45,
            penguasaan_bola_tamu=55,
            tembakan_tuan_rumah=7,
            tembakan_tamu=9,
            on_target_tuan_rumah=2,
            on_target_tamu=1,
            akurasi_umpan_tuan_rumah=73,
            akurasi_umpan_tamu=79,
            pelanggaran_tuan_rumah=5,
            pelanggaran_tamu=12,
            kartu_kuning_tuan_rumah=1,
            kartu_kuning_tamu=6,
            kartu_merah_tuan_rumah=1,
            kartu_merah_tamu=0,
            offside_tuan_rumah=2,
            offside_tamu=3,
            corner_tuan_rumah=1,
            corner_tamu=4,
        )
        self.assertEqual(pertandingan.jenis_pertandingan, "kualifikasi piala dunia")
        self.assertEqual(pertandingan.tim_tuan_rumah, "Irak")
        self.assertEqual(pertandingan.tim_tamu, "Indonesia")
        self.assertEqual(pertandingan.bendera_tuan_rumah, "https://ssl.gstatic.com/onebox/media/sports/logos/kErkaIWGPh_VGrd4T6NwUA_96x96.png")
        self.assertEqual(pertandingan.bendera_tamu, "https://ssl.gstatic.com/onebox/media/sports/logos/S5ivsscrfCG1mgqceKMPlQ_96x96.png")
        self.assertEqual(pertandingan.tanggal, "12/10/2025")
        self.assertEqual(pertandingan.stadion, "King Abdullah Sports City")
        self.assertEqual(pertandingan.skor_tuan_rumah, 1)
        self.assertEqual(pertandingan.skor_tamu, 0)
        self.assertEqual(pertandingan.pencetak_gol_tuan_rumah, "Zidane Iqbal 76'")
        self.assertEqual(pertandingan.pencetak_gol_tamu, "")
        self.assertEqual(pertandingan.starter_tuan_rumah, "Jalal Hasan;Hussein Ali;Zaid Tahseen;Merchas Doski;Manaf Younis;Bashar Resan;Amir Al-Ammari;Kevin Yakob;Ibrahim Bayesh;Mohamed Ali;Sherko Karim Gubari")
        self.assertEqual(pertandingan.starter_tamu, "Maarten Paes;Dean James;Jay Idzes;Kevin Diks;Rizky Ridho;Thom Haye;Calvin Verdonk;Joey Pelupessy; Ricky Kambuaya;Eliano Reijnders;Mauro Ziljstra")
        self.assertEqual(pertandingan.pengganti_tuan_rumah, "Rebin Sulaka;Youssef Amyn;Zidane Iqbal;Ali jAsim;Amar Muhsin;Fahad Talib;Akam Hashim;Hasan Abdulkareem;Ahmed Al-Hajjaj;Aimar Sher;Mustafa Saadoon;Ahmed Basil")
        self.assertEqual(pertandingan.pengganti_tamu, "Ramadhan Sananta;Miliano Jonathans;Ole Romeny;Ragnar Oratmangoen;Nathan Tjoe-A-On;Jordi Amat;Sandy Walsh;Stefano Lilipaly;Ernando Ari Sutaryadi;Nadeo Argawinata;Marc klok;Shayne Pattynama")
        self.assertEqual(pertandingan.manajer_tuan_rumah, "Graham Arnold")
        self.assertEqual(pertandingan.manajer_tamu, "Patrick Kluivert")
        self.assertEqual(pertandingan.highlight, "youtube.com/watch?v=YLPOfyDxYXg&feature=onebox")
        self.assertEqual(pertandingan.penguasaan_bola_tuan_rumah, 45)
        self.assertEqual(pertandingan.penguasaan_bola_tamu, 55)
        self.assertEqual(pertandingan.tembakan_tuan_rumah, 7)
        self.assertEqual(pertandingan.tembakan_tamu, 9)
        self.assertEqual(pertandingan.on_target_tuan_rumah, 2)
        self.assertEqual(pertandingan.on_target_tamu, 1)
        self.assertEqual(pertandingan.akurasi_umpan_tuan_rumah, 73)
        self.assertEqual(pertandingan.akurasi_umpan_tamu, 79)
        self.assertEqual(pertandingan.pelanggaran_tuan_rumah, 5)
        self.assertEqual(pertandingan.pelanggaran_tamu, 12)
        self.assertEqual(pertandingan.kartu_kuning_tuan_rumah, 1)
        self.assertEqual(pertandingan.kartu_kuning_tamu, 6)
        self.assertEqual(pertandingan.kartu_merah_tuan_rumah, 1)
        self.assertEqual(pertandingan.kartu_merah_tamu, 0)
        self.assertEqual(pertandingan.offside_tuan_rumah, 2)
        self.assertEqual(pertandingan.offside_tamu, 3)
        self.assertEqual(pertandingan.corner_tuan_rumah, 1)
        self.assertEqual(pertandingan.corner_tamu, 4)


        
    def test_pertandingan_default_values(self):
        pertandingan = Pertandingan.objects.create(
            jenis_pertandingan="kualifikasi piala dunia",
            tim_tuan_rumah="Irak",
            tim_tamu="Indonesia",
        )
        self.assertEqual(pertandingan.penguasaan_bola_tuan_rumah, 0)
        self.assertEqual(pertandingan.penguasaan_bola_tamu, 0)
        self.assertEqual(pertandingan.tembakan_tuan_rumah,0)
        self.assertEqual(pertandingan.tembakan_tamu,0)
        self.assertEqual(pertandingan.on_target_tuan_rumah,0)
        self.assertEqual(pertandingan.on_target_tamu,0)
        self.assertEqual(pertandingan.akurasi_umpan_tuan_rumah, 0)
        self.assertEqual(pertandingan.akurasi_umpan_tamu, 0)
        self.assertEqual(pertandingan.pelanggaran_tuan_rumah,0)
        self.assertEqual(pertandingan.pelanggaran_tamu, 0)
        self.assertEqual(pertandingan.kartu_kuning_tuan_rumah,0)
        self.assertEqual(pertandingan.kartu_kuning_tamu,0)
        self.assertEqual(pertandingan.kartu_merah_tuan_rumah,0)
        self.assertEqual(pertandingan.kartu_merah_tamu,0)
        self.assertEqual(pertandingan.offside_tuan_rumah,0)
        self.assertEqual(pertandingan.offside_tamu,0)
        self.assertEqual(pertandingan.corner_tuan_rumah,0)
        self.assertEqual(pertandingan.corner_tamu,0)


class MatchViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.match1_uuid = uuid.uuid4()
        self.match2_uuid = uuid.uuid4()

        # Data dummy
        self.pertandingan1 = Pertandingan.objects.create(
            id=self.match1_uuid,
            jenis_pertandingan="Kualifikasi Piala Dunia",
            tim_tuan_rumah="Indonesia",
            tim_tamu="Irak",
            tanggal="2025/12/01",
            skor_tuan_rumah=0,
            skor_tamu=2,
        )
        self.pertandingan2 = Pertandingan.objects.create(
            id=self.match2_uuid,
            jenis_pertandingan="Piala Asia",
            tim_tuan_rumah="Jepang",
            tim_tamu="Indonesia",
            tanggal="2025/12/01",
            skor_tuan_rumah=3,
            skor_tamu=1,
        )
        
        # Data valid untuk form POST
        self.valid_form_data = {
            "jenis_pertandingan": "Persahabatan",
            "tim_tuan_rumah": "Timor Leste",
            "tim_tamu": "Indonesia",
            "tanggal": "2025/12/01",
            "skor_tuan_rumah": 0,
            "skor_tamu": 5,
        }
        
        # Data tidak valid untuk form POST 
        self.invalid_form_data = {
            "jenis_pertandingan": "Test Invalid",
            "tim_tuan_rumah": "Tim A",
            "tim_tamu": "Tim B",
            "tanggal": 123, 
            "skor_tuan_rumah": 1,
            "skor_tamu": 1,
        }
    
    # Berhasil Menghapus dan redirect
    def test_delete_match_view_success(self):
        match_to_delete_id = self.pertandingan1.id 
        url = reverse('match:delete_match', args=[match_to_delete_id])
        initial_count = Pertandingan.objects.count()

        response = self.client.post(url) 

        # Cek status dan URL redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('match:show_match'))

        # Cek apakah objek sudah terhapus dari database
        self.assertEqual(Pertandingan.objects.count(), initial_count - 1)
        with self.assertRaises(Pertandingan.DoesNotExist):
            Pertandingan.objects.get(pk=match_to_delete_id)

    # Delete match yang tidak ada
    def test_delete_match_view_not_found(self):
        non_existent_uuid = uuid.uuid4() # Buat UUID acak yang tidak ada
        url = reverse('match:delete_match', args=[non_existent_uuid])

        # Coba akses URL dengan id yang tidak ada
        response = self.client.post(url)

        # Cek status
        self.assertEqual(response.status_code, 404)
        