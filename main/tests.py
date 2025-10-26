from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import LandingPage
import json

class MainViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('main:login_user')
        self.logout_url = reverse('main:logout_user')
        self.register_url = reverse('main:register_user')
        self.main_url = reverse('main:show_main')
        self.landing_url = reverse('main:show_landingpage')
        self.login_ajax_url = reverse('main:login_ajax')
        self.register_ajax_url = reverse('main:register_ajax')
        self.json_url = reverse('main:show_json')
        self.xml_url = reverse('main:show_xml')
        self.landing = LandingPage.objects.create(title="Welcome", content="Hello World")

    # ---------- AUTH TESTS ----------
    def test_register_user_success(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_user_fail_password_mismatch(self):
        response = self.client.post(self.register_ajax_url, {
            'username': 'user1',
            'password1': 'abc',
            'password2': 'def'
        })
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['status'])

    def test_login_user_success(self):
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.main_url)

    def test_login_user_fail(self):
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_login_ajax_success(self):
        response = self.client.post(self.login_ajax_url, {
            'username': self.username,
            'password': self.password
        })
        data = response.json()
        self.assertTrue(data['status'])
        self.assertEqual(response.status_code, 200)

    def test_login_ajax_fail(self):
        response = self.client.post(self.login_ajax_url, {
            'username': self.username,
            'password': 'wrong'
        })
        data = response.json()
        self.assertFalse(data['status'])
        self.assertEqual(response.status_code, 401)

    def test_logout_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_register_ajax_success(self):
        response = self.client.post(self.register_ajax_url, {
            'username': 'ajaxuser',
            'password1': 'ajaxpassword123',
            'password2': 'ajaxpassword123'
        })
        data = response.json()
        self.assertTrue(data['status'])
        self.assertEqual(response.status_code, 201)

    def test_register_ajax_username_exists(self):
        response = self.client.post(self.register_ajax_url, {
            'username': self.username,
            'password1': 'somepassword123',
            'password2': 'somepassword123'
        })
        data = response.json()
        self.assertFalse(data['status'])
        self.assertEqual(response.status_code, 400)

    def test_register_ajax_short_password(self):
        response = self.client.post(self.register_ajax_url, {
            'username': 'tiny',
            'password1': '123',
            'password2': '123'
        })
        data = response.json()
        self.assertFalse(data['status'])
        self.assertEqual(response.status_code, 400)

    # ---------- MAIN PAGE TESTS ----------
    def test_show_main_requires_login(self):
        response = self.client.get(self.main_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

    def test_show_main_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.main_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.username)

    def test_show_landingpage_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.landing_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome")

    # ---------- JSON/XML TESTS ----------
    def test_show_json_returns_json(self):
        response = self.client.get(self.json_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertGreaterEqual(len(data), 1)

    def test_show_xml_returns_xml(self):
        response = self.client.get(self.xml_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<?xml", response.content)

