from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal

from .models import Player

User = get_user_model()


class BaseSetup(TestCase):
    def setUp(self):
        self.client = Client()
        # buat user & login karena beberapa view pakai @login_required
        self.user = User.objects.create_user(
            username="tester", email="t@example.com", password="pass12345"
        )
        self.client.login(username="tester", password="pass12345")

        self.player = Player.objects.create(
            nama="Marselino Ferdinan",
            posisi="FW",
            klub="AS Trencin",
            umur=21,
            market_value=Decimal("2.61"),
            foto="https://example.com/marselino.jpg",
        )


class PlayerModelTest(TestCase):
    def test_create_player(self):
        p = Player.objects.create(
            nama="Maarten Paes",
            posisi="GK",
            klub="FC Dallas",
            umur=27,
            market_value=Decimal("31.29"),
            foto="",
        )
        self.assertTrue(p.id)  # UUID terset
        self.assertEqual(p.posisi, "GK")
        self.assertEqual(p.umur, 27)

    def test_str_not_empty(self):
        p = Player.objects.create(
            nama="Emil Audero",
            posisi="GK",
            klub="Cremonese",
            umur=28,
            market_value=Decimal("55.62"),
        )
        self.assertTrue(str(p))  # tidak kosong


class UrlsResolveTest(BaseSetup):
    def test_urls_exist(self):
        # pastikan nama URL tidak typo
        self.assertTrue(reverse("ProfileAktif:show_main"))
        self.assertTrue(reverse("ProfileAktif:show_json"))
        self.assertTrue(reverse("ProfileAktif:create_player"))
        self.assertTrue(reverse("ProfileAktif:show_player", kwargs={"id": self.player.id}))

        # NOTE: ini akan berhasil hanya jika urls.py sudah pakai player_id (bukan news_id)
        # reverse("ProfileAktif:show_json_by_id", kwargs={"player_id": str(self.player.id)})
        # reverse("ProfileAktif:show_xml_by_id", kwargs={"player_id": str(self.player.id)})


class ViewsTest(BaseSetup):
    def test_show_main_ok(self):
        url = reverse("ProfileAktif:show_main")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "main.html")
        self.assertContains(res, "Pemain Aktif Timnas Indonesia")

    def test_show_player_ok(self):
        url = reverse("ProfileAktif:show_player", kwargs={"id": self.player.id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "player_detail.html")
        self.assertContains(res, self.player.nama)

    def test_show_json_shape(self):
        url = reverse("ProfileAktif:show_json")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res["Content-Type"], "application/json")
        data = res.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        first = data[0]
        # kunci-kunci penting
        for key in ["id", "nama", "posisi", "klub", "umur", "market_value", "foto"]:
            self.assertIn(key, first)
        # posisi human readable (bukan kode)
        self.assertIn(first["posisi"], ["Goalkeeper", "Defender", "Midfielder", "Forward"])

    def test_create_player_valid_ajax(self):
        url = reverse("ProfileAktif:create_player")
        payload = {
            "nama": "Iqbal Gwijangge",
            "posisi": "DF",
            "klub": "Tim U19",
            "umur": 18,
            "market_value": "1.25",
            "foto": "https://example.com/iqbal.jpg",
        }
        res = self.client.post(
            url,
            data=payload,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertTrue(body.get("success"))
        self.assertTrue(Player.objects.filter(nama="Iqbal Gwijangge", klub="Tim U19").exists())

    def test_create_player_invalid_ajax(self):
        url = reverse("ProfileAktif:create_player")
        payload = {
            "nama": "",              # invalid
            "posisi": "MF",
            "klub": "Persija",
            "umur": 22,
            "market_value": "3.40",
        }
        res = self.client.post(
            url,
            data=payload,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(res.status_code, 400)
        body = res.json()
        self.assertFalse(body.get("success"))
        self.assertIn("nama", body.get("errors", {}))

    def test_create_player_get_renders_form(self):
        url = reverse("ProfileAktif:create_player")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "create_player.html")
