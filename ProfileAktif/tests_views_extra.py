from decimal import Decimal
import uuid

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from ProfileAktif.models import Player


class ProfileAktifViewsCoverageTests(TestCase):
    def setUp(self):
        # user + login karena show_main/show_player dilindungi @login_required
        self.client = Client()
        self.user = User.objects.create_user(username="tester", password="secret123")
        self.client.login(username="tester", password="secret123")

        # URL name shortcuts
        self.url_show_main = reverse("ProfileAktif:show_main")
        self.url_create_player = reverse("ProfileAktif:create_player")
        self.url_show_json = reverse("ProfileAktif:show_json")
        self.url_show_xml = reverse("ProfileAktif:show_xml")

    # --- show_main ---

    def test_show_main_when_empty_uses_dummy(self):
        # DB kosong -> cabang if not players.exists()
        resp = self.client.get(self.url_show_main)
        self.assertEqual(resp.status_code, 200)
        # kita cukup memastikan templatenya render OK (branch ke-cover)

    def test_show_main_when_has_players(self):
        Player.objects.create(
            nama="Asnawi",
            posisi="DF",
            klub="Jeonnam Dragons",
            umur=25,
            market_value=Decimal("2.00"),
            foto="https://example.com/asnawi.jpg",
        )
        resp = self.client.get(self.url_show_main)
        self.assertEqual(resp.status_code, 200)

    # --- create_player ---

    def test_create_player_get_renders_form(self):
        resp = self.client.get(self.url_create_player)
        self.assertEqual(resp.status_code, 200)
        # cek field 'nama' ada
        self.assertContains(resp, 'id="id_nama"')
        # opsional: cek label default
        self.assertContains(resp, "Nama:")


    def test_create_player_post_valid_returns_json_success(self):
        payload = {
            "nama": "Marselino",
            "posisi": "MF",
            "klub": "KMSK Deinze",
            "umur": 20,
            "market_value": "2.50",
            "foto": "https://example.com/marselino.jpg",
        }
        resp = self.client.post(self.url_create_player, payload, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])

        # ambil dari DB dan cocokkan persis
        p = Player.objects.get(nama="Marselino")
        self.assertEqual(
            data,
            {
                "success": True,
                "player_id": str(p.id),  # <- pakai str(UUID) biar sama dengan response
                "message": "Pemain berhasil ditambahkan",
            },
        )


    def test_create_player_post_invalid_returns_400_and_errors(self):
        # Missing required fields
        payload = {
            "nama": "",
            "posisi": "",
            "klub": "",
            "umur": "",
            "market_value": "",
            "foto": "",
        }
        resp = self.client.post(self.url_create_player, payload, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(resp.status_code, 400)
        data = resp.json()
        self.assertFalse(data["success"])
        self.assertIn("errors", data)

    # --- show_player ---

    def test_show_player_with_existing_id(self):
        p = Player.objects.create(
            nama="Rizky Ridho",
            posisi="DF",
            klub="Persija",
            umur=23,
            market_value=Decimal("1.75"),
            foto="https://example.com/ridho.jpg",
        )
        url = reverse("ProfileAktif:show_player", args=[str(p.id)])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Rizky Ridho")

    def test_show_player_with_missing_id_uses_dummy(self):
        # pakai UUID random supaya trigger except Player.DoesNotExist
        random_id = uuid.uuid4()
        url = reverse("ProfileAktif:show_player", args=[str(random_id)])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # fallback dummy mengandung "Marselino"
        self.assertContains(resp, "Marselino")

    # --- show_json & show_xml ---

    def test_show_json_structure_and_display_values(self):
        p = Player.objects.create(
            nama="Elkan Baggott",
            posisi="DF",
            klub="Ipswich",
            umur=22,
            market_value=Decimal("3.00"),
            foto="https://example.com/elkan.jpg",
        )
        resp = self.client.get(self.url_show_json)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        # pastikan posisi menggunakan display (Defender), bukan 'DF'
        one = data[0]
        self.assertIn("posisi", one)
        self.assertIn(one["posisi"], ["Goalkeeper", "Defender", "Midfielder", "Forward"])

    def test_show_xml_returns_xml(self):
        Player.objects.create(
            nama="Sandy",
            posisi="GK",
            klub="Bali United",
            umur=27,
            market_value=Decimal("1.10"),
            foto="https://example.com/sandy.jpg",
        )
        resp = self.client.get(self.url_show_xml)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "application/xml")
        self.assertIn(b"<django-objects", resp.content)

    # --- show_xml_by_id / show_json_by_id ---

    def test_show_xml_by_id_found_and_not_found(self):
        p = Player.objects.create(
            nama="Witan",
            posisi="FW",
            klub="Bhayangkara",
            umur=23,
            market_value=Decimal("1.20"),
            foto="https://example.com/witan.jpg",
        )
        url_found = reverse("ProfileAktif:show_xml_by_id", args=[str(p.id)])
        resp_ok = self.client.get(url_found)
        self.assertEqual(resp_ok.status_code, 200)
        self.assertEqual(resp_ok["Content-Type"], "application/xml")

        url_404 = reverse("ProfileAktif:show_xml_by_id", args=[str(uuid.uuid4())])
        resp_404 = self.client.get(url_404)
        # catatan: view kamu pakai filter() dan tidak raise DoesNotExist;
        # tapi kita tetap cek 200 agar barisnya ke-eksekusi. Kalau ingin 404, ubah view.
        self.assertEqual(resp_404.status_code, 200)  # atau sesuaikan jika kamu ubah view

    def test_show_json_by_id_found_and_not_found(self):
        p = Player.objects.create(
            nama="Pratama Arhan",
            posisi="DF",
            klub="Consadole Sapporo",
            umur=22,
            market_value=Decimal("2.00"),
            foto="https://example.com/arhan.jpg",
        )
        url_found = reverse("ProfileAktif:show_json_by_id", args=[str(p.id)])
        resp_ok = self.client.get(url_found)
        self.assertEqual(resp_ok.status_code, 200)
        self.assertEqual(resp_ok["Content-Type"], "application/json")

        url_404 = reverse("ProfileAktif:show_json_by_id", args=[str(uuid.uuid4())])
        resp_404 = self.client.get(url_404)
        self.assertEqual(resp_404.status_code, 404)
