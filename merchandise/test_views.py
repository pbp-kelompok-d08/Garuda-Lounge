from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.html import escape
from .models import Merch
import json

class MerchViewsTest(TestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.other_user = User.objects.create_user(username="other", password="pass123")

        # Create sample merch
        self.merch = Merch.objects.create(
            name="Jersey A",
            description="Official jersey",
            category="jersey",
            price=150000,
            thumbnail="https://example.com/img.jpg",
            product_link="https://example.com/item",
            user=self.user
        )

        self.client = Client()

    # ---------- LOGIN REQUIRED ----------
    def test_show_merch_requires_login(self):
        response = self.client.get(reverse("merchandise:show_merch"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/login"))

    # ---------- SHOW LIST ----------
    def test_show_merch_all_and_my_filter(self):
        self.client.login(username="tester", password="pass123")
        # all
        res_all = self.client.get(reverse("merchandise:show_merch"), {"filter": "all"})
        self.assertEqual(res_all.status_code, 200)
        self.assertContains(res_all, "Jersey A")

        # my
        res_my = self.client.get(reverse("merchandise:show_merch"), {"filter": "my"})
        self.assertContains(res_my, "Jersey A")

    # ---------- DETAIL ----------
    def test_show_merch_detail_view(self):
        self.client.login(username="tester", password="pass123")
        url = reverse("merchandise:show_merch_detail", args=[self.merch.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Jersey A")

    # ---------- CREATE ----------
    def test_create_merch_valid_post(self):
        self.client.login(username="tester", password="pass123")
        data = {
            "name": "Ball X",
            "description": "Football",
            "category": "ball",
            "price": 99999,
            "thumbnail": "https://example.com/ball.jpg",
            "product_link": "https://example.com/ball",
        }
        res = self.client.post(reverse("merchandise:create_merch"), data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Merch.objects.filter(name="Ball X").exists())

    def test_create_merch_invalid_post(self):
        self.client.login(username="tester", password="pass123")
        res = self.client.post(reverse("merchandise:create_merch"), {"name": ""})
        self.assertEqual(res.status_code, 200)  # Renders form again
        self.assertContains(res, "name")

    # ---------- EDIT ----------
    def test_edit_merch_valid_post(self):
        self.client.login(username="tester", password="pass123")
        url = reverse("merchandise:edit_merch", args=[self.merch.id])
        data = {
            "name": "Jersey Updated",
            "description": "Updated desc",
            "category": "jersey",
            "price": 200000,
            "thumbnail": self.merch.thumbnail,
            "product_link": self.merch.product_link,
        }
        res = self.client.post(url, data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.merch.refresh_from_db()
        self.assertEqual(self.merch.name, "Jersey Updated")

    # ---------- DELETE ----------
    def test_delete_merch_success(self):
        self.client.login(username="tester", password="pass123")
        url = reverse("merchandise:delete_merch", args=[self.merch.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Merch.objects.filter(pk=self.merch.id).exists())

    def test_delete_merch_forbidden_if_not_owner(self):
        self.client.login(username="other", password="pass123")
        url = reverse("merchandise:delete_merch", args=[self.merch.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 403)

    def test_delete_merch_not_found(self):
        self.client.login(username="tester", password="pass123")
        url = reverse("merchandise:delete_merch", args=["11111111-1111-1111-1111-111111111111"])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 404)

    # ---------- AJAX CREATE ----------
    def test_add_merch_entry_ajax_success(self):
        self.client.login(username="tester", password="pass123")
        data = {
            "name": "Scarf Z",
            "description": "Limited scarf",
            "category": "scarf",
            "price": 120000,
            "thumbnail": "https://example.com/scarf.jpg",
            "product_link": "https://example.com/scarf",
        }
        url = reverse("merchandise:add_merch_entry_ajax")
        res = self.client.post(url, data, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(res.status_code, 201)
        body = json.loads(res.content)
        self.assertIn("name", body)
        self.assertEqual(body["name"], "Scarf Z")

    def test_add_merch_entry_ajax_missing_field(self):
        self.client.login(username="tester", password="pass123")
        url = reverse("merchandise:add_merch_entry_ajax")
        res = self.client.post(url, {"name": ""})
        self.assertEqual(res.status_code, 400)

    # ---------- JSON/XML ----------
    def test_show_json_endpoint(self):
        url = reverse("merchandise:show_json")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(data[0]["name"], self.merch.name)

    def test_show_xml_endpoint(self):
        url = reverse("merchandise:show_xml")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"<object", res.content)

    def test_show_json_by_id(self):
        url = reverse("merchandise:show_json_by_id", args=[self.merch.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(data["id"], str(self.merch.id))

    def test_show_xml_by_id(self):
        url = reverse("merchandise:show_xml_by_id", args=[self.merch.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"<object", res.content)
