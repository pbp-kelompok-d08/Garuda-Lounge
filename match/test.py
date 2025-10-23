from django.test import TestCase, Client
from .models import Pertandingan

class MatchTest(TestCase):
    def test_match_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_match_using_match_template(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'match.html')

    def test_nonexistent_page(self):
        response = Client().get('/burhan_always_exists/')
        self.assertEqual(response.status_code, 404)

    def test_pertandingan_creation(self):
        pertandingan = Pertandingan.objects.create(
          title="BURHAN FC MENANG",
          content="BURHAN FC 1-0 PANDA BC",
          category="match",
          pertandingan_views=1001,
          is_featured=True
        )
        self.assertTrue(pertandingan.is_pertandingan_hot)
        self.assertEqual(pertandingan.category, "match")
        self.assertTrue(pertandingan.is_featured)
        
    def test_pertandingan_default_values(self):
        pertandingan = Pertandingan.objects.create(
          title="Test Pertandingan",
          content="Test content"
        )
        self.assertEqual(pertandingan.category, "update")
        self.assertEqual(pertandingan.pertandingan_views, 0)
        self.assertFalse(pertandingan.is_featured)
        self.assertFalse(pertandingan.is_pertandingan_hot)
        
    def test_increment_views(self):
        pertandingan = Pertandingan.objects.create(
          title="Test Pertandingan",
          content="Test content"
        )
        initial_views = pertandingan.pertandingan_views
        pertandingan.increment_views()
        self.assertEqual(pertandingan.pertandingan_views, initial_views + 1)
        
    def test_is_pertandingan_hot_threshold(self):
        # Test pertandingan with exactly 20 views (should not be hot)
        pertandingan_20 = Pertandingan.objects.create(
          title="Pertandingan with 20 views",
          content="Test content",
          pertandingan_views=20
        )
        self.assertFalse(pertandingan_20.is_pertandingan_hot)
        
        # Test pertandingan with 21 views (should be hot)
        pertandingan_21 = Pertandingan.objects.create(
          title="Pertandingan with 21 views", 
          content="Test content",
          pertandingan_views=21
        )
        self.assertTrue(pertandingan_21.is_pertandingan_hot)