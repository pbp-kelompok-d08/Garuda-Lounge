import uuid
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import serializers
from .models import LegendPlayer
from .forms import LegendPlayerForm


# --- BASE SETUP ---
class BaseSetup(TestCase):
    def setUp(self):
        self.client = Client()

        # create and login user
        self.user = User.objects.create_user(
            username="tester", password="12345"
        )
        self.client.login(username="tester", password="12345")

        # create one legend
        self.legend = LegendPlayer.objects.create(
            name="Bambang Pamungkas",
            position=LegendPlayer.Position.PENYERANG,
            club="Persija",
            age=40,
            is_legend=True,
            photo_url=None
        )


# --- MODEL TEST ---
class ModelTest(BaseSetup):
    def test_str_output(self):
        self.assertEqual(
            str(self.legend),
            "Bambang Pamungkas (Penyerang)"
        )

    def test_default_is_legend_true(self):
        p = LegendPlayer.objects.create(
            name="Kurniawan",
            position=LegendPlayer.Position.PENYERANG,
        )
        self.assertTrue(p.is_legend)


# --- URL TEST ---
class UrlTest(BaseSetup):
    def test_urls_exists(self):
        self.assertTrue(reverse('ProfileLegend:show_profile_legend'))
        self.assertTrue(reverse('ProfileLegend:show_json'))
        self.assertTrue(reverse('ProfileLegend:add_legend_ajax'))
        self.assertTrue(reverse('ProfileLegend:create_legend'))
        self.assertTrue(
            reverse('ProfileLegend:show_legend_detail', args=[self.legend.id])
        )
        self.assertTrue(
            reverse('ProfileLegend:show_json_by_id', args=[self.legend.id])
        )


# --- VIEW TEST ---
class ViewTest(BaseSetup):
    def test_show_profile_legend(self):
        res = self.client.get(reverse('ProfileLegend:show_profile_legend'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "show_profile_legend.html")
        self.assertContains(res, "Bambang Pamungkas")

    def test_legend_detail_found(self):
        url = reverse('ProfileLegend:show_legend_detail', args=[self.legend.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "legend_detail.html")
        self.assertContains(res, "Persija Jakarta")

    def test_legend_detail_dummy_if_not_exists(self):
        fake = uuid.uuid4()
        url = reverse('ProfileLegend:show_legend_detail', args=[fake])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Bambang Pamungkas")  # dummy fallback
        self.assertIsInstance(res.context['player'], dict)
    
    def test_create_legend_page_GET(self):
        res = self.client.get(reverse('ProfileLegend:create_legend'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "create_legend.html")
        self.assertIsInstance(res.context['form'], LegendPlayerForm)

# --- JSON TEST ---
class JsonTest(BaseSetup):
    def test_json_structure(self):
        res = self.client.get(reverse('ProfileLegend:show_json'))
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIsInstance(data, list)

        first = data[0]
        for key in ["id", "name", "position", "club", "age", "photo_url", "is_legend"]:
            self.assertIn(key, first)

    def test_json_by_id(self):
        url = reverse('ProfileLegend:show_json_by_id', args=[self.legend.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

        expected = serializers.serialize("json", [self.legend])
        self.assertJSONEqual(res.content.decode("utf-8"), expected)


# --- FORM TEST ---
class FormTest(BaseSetup):
    def test_form_valid(self):
        form = LegendPlayerForm(data={
            "name": "Rudi",
            "position": "Bek",
            "club": "Arema",
            "age": 30,
            "photo_url": "",
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_name(self):
        form = LegendPlayerForm(data={
            "name": "",
            "position": "Bek",
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


# --- AJAX TEST ---
class AjaxTest(BaseSetup):
    def test_ajax_add_success(self):
        before = LegendPlayer.objects.count()

        res = self.client.post(
            reverse('ProfileLegend:add_legend_ajax'),
            data={
                "name": "Bima Sakti",
                "position": "Gelandang",
                "club": "Perseba Bangkalan",
                "age": 49,
                "photo_url": ""
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(LegendPlayer.objects.count(), before + 1)
        self.assertTrue(LegendPlayer.objects.filter(name="Bima Sakti").exists())

    def test_ajax_rejects_get(self):
        res = self.client.get(reverse('ProfileLegend:add_legend_ajax'))
        self.assertEqual(res.status_code, 405)