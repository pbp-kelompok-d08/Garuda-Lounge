# tests.py
from django.test import TestCase, Client, LiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from .models import News

# =========================
# Unit & Integration (Client)
# =========================

class NewsUnitIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testadmin", password="testpassword")
        self.news = News.objects.create(
            title="UnitTest News",
            content="Unit test content",
            user=self.user,
            category=getattr(News, "category", "update") if hasattr(News, "category") else "update",
        )

    def test_login_required_on_main(self):
        url = reverse("news:show_news_main")
        r = self.client.get(url)
        self.assertIn(r.status_code, (301, 302))  # redirect ke login

    def test_list_after_login(self):
        """
        Banyak halaman utama di-hydrate via JS -> judul bisa tidak ada di HTML awal.
        Perbaikan: cek 200 di main page, lalu verifikasi data lewat endpoint JSON.
        """
        self.client.login(username="testadmin", password="testpassword")
        url_main = reverse("news:show_news_main")
        r_main = self.client.get(url_main)
        self.assertEqual(r_main.status_code, 200)

        html = r_main.content.decode()
        if "UnitTest News" not in html:
            # fallback ke JSON jika list diisi via JS
            url_json = reverse("news:show_json")
            r_json = self.client.get(url_json)
            self.assertEqual(r_json.status_code, 200)
            data = r_json.json()
            titles = {item.get("title") for item in data}
            self.assertIn("UnitTest News", titles)
        else:
            self.assertIn("UnitTest News", html)

    def test_create_news_via_post(self):
        self.client.login(username="testadmin", password="testpassword")
        url = reverse("news:create_news")
        payload = {
            "title": "Created From Client",
            "content": "Body",
            "category": "match",
            "thumbnail": "https://example.com/i.jpg",
            "is_featured": "on",
        }
        r = self.client.post(url, data=payload)
        self.assertIn(r.status_code, (302, 303))
        self.assertTrue(News.objects.filter(title="Created From Client").exists())

    def test_detail_by_id_increments_views(self):
        self.client.login(username="testadmin", password="testpassword")
        url = reverse("news:show_news_detail", kwargs={"id": self.news.id})
        before = self.news.news_views
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.news.refresh_from_db()
        self.assertEqual(self.news.news_views, before + 1)

    def test_slug_and_get_absolute_url(self):
        n2 = News.objects.create(title="Same Title", content="x", user=self.user, category="update")
        n3 = News.objects.create(title="Same Title", content="y", user=self.user, category="update")
        self.assertTrue(n2.slug)
        self.assertTrue(n3.slug)
        self.assertNotEqual(n2.slug, n3.slug)
        self.assertIn(n2.slug, n2.get_absolute_url())


# =========================
# Extra branches to boost coverage (views & models)
# =========================
import json, uuid
from django.contrib import admin

class NewsExtraBranchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("u", password="p")
        self.client.login(username="u", password="p")
        self.news = News.objects.create(
            user=self.user, title="N1", content="C1", category="update"
        )

    # --- show_news_main filters ---
    def test_main_page_filter_all(self):
        r = self.client.get(reverse("news:show_news_main") + "?filter=all")
        self.assertEqual(r.status_code, 200)

    def test_main_page_filter_my(self):
        r = self.client.get(reverse("news:show_news_main") + "?filter=my")
        self.assertEqual(r.status_code, 200)

    # --- detail slug 404 ---
    def test_detail_by_slug_not_found_404(self):
        r = self.client.get(reverse("news:show_news_detail_slug", kwargs={"slug": "tidak-ada"}))
        self.assertEqual(r.status_code, 404)

    # --- create_news: GET form + POST invalid ---
    def test_create_news_get_form_ok(self):
        r = self.client.get(reverse("news:create_news"))
        self.assertEqual(r.status_code, 200)
        # pastikan context form ada (kalau view pakai context "form")
        if hasattr(r, "context") and r.context is not None:
            self.assertTrue("form" in r.context)

    def test_create_news_post_invalid_shows_errors(self):
        r = self.client.post(reverse("news:create_news"), data={
            "title": "", "content": "", "category": ""   # required -> invalid
        })
        self.assertEqual(r.status_code, 200)
        self.assertIn("error", r.content.decode().lower())

    # --- edit_news: POST invalid (tetap 200 + errors) ---
    def test_edit_news_post_invalid(self):
        r = self.client.post(reverse("news:edit_news", args=[self.news.id]), data={
            "title": "", "content": "", "category": ""
        })
        self.assertEqual(r.status_code, 200)
        self.assertIn("error", r.content.decode().lower())

    # --- delete_news: GET biasanya tak diizinkan / guarded ---
    def test_delete_news_get_method_guard(self):
        r = self.client.get(reverse("news:delete_news", args=[self.news.id]))
        self.assertIn(r.status_code, (200, 403, 405))

    # --- add_news_entry_ajax: variasi konten & auth ---
    def test_add_news_entry_ajax_malformed_json(self):
        url = reverse("news:add_news_entry_ajax")
        r = self.client.post(url, data="{malformed", content_type="application/json")
        self.assertIn(r.status_code, (400, 422))

    def test_add_news_entry_ajax_requires_login(self):
        self.client.logout()
        url = reverse("news:add_news_entry_ajax")
        r = self.client.post(url, data=json.dumps({
            "title": "A", "content": "B", "category": "update"
        }), content_type="application/json")
        self.assertIn(r.status_code, (301, 302))  # redirected to login

    # --- comments endpoints ---
    def test_add_comment_blank_returns_400(self):
        url = reverse("news:add_comment", args=[self.news.id])
        r = self.client.post(url, data=json.dumps({"content": ""}),
                             content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def test_get_comments_ok(self):
        url = reverse("news:get_comments", args=[self.news.id])
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertIn("comments", r.json())

    # --- JSON/XML list & by id ---
    def test_show_json_list_ok(self):
        r = self.client.get(reverse("news:show_json"))
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)

    def test_show_json_by_id_ok(self):
        r = self.client.get(reverse("news:show_json_by_id", kwargs={"id": self.news.id}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["id"], str(self.news.id))

    def test_show_json_by_id_invalid_uuid_404(self):
        bad = uuid.uuid4()
        self.news.delete()
        r = self.client.get(reverse("news:show_json_by_id", kwargs={"id": bad}))
        self.assertEqual(r.status_code, 404)

    def test_show_xml_list_ok(self):
        r = self.client.get(reverse("news:show_xml"))
        self.assertEqual(r.status_code, 200)
        self.assertIn("application/xml", r["Content-Type"])

    def test_show_xml_by_id_ok(self):
        r = self.client.get(reverse("news:show_xml_by_id", kwargs={"news_id": self.news.id}))
        self.assertEqual(r.status_code, 200)
        self.assertIn("application/xml", r["Content-Type"])

    # --- models: __str__, thumbnail default, is_hot branch ---
    def test_model_str_and_is_hot_branch(self):
        n = News.objects.create(user=self.user, title="T", content="C", category="update")
        self.assertIn("T", str(n))
        for _ in range(30):
            n.increment_views()
        n.refresh_from_db()
        self.assertTrue(n.is_hot)

    # --- admin registered (menaikkan sedikit coverage admin.py) ---
    def test_news_admin_registered(self):
        self.assertIn(News, admin.site._registry)


# =========================
# Functional (Selenium) — headless & auto-skip bila driver tak ada
# =========================

from selenium.webdriver.chrome.options import Options
try:
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    _HAS_WDM = True
except Exception:
    _HAS_WDM = False


class FootballNewsFunctionalTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._skip = False
        try:
            opts = Options()
            opts.add_argument("--headless=new")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            if _HAS_WDM:
                service = Service(ChromeDriverManager().install())
                cls.browser = webdriver.Chrome(service=service, options=opts)
            else:
                cls.browser = webdriver.Chrome(options=opts)
        except Exception:
            cls._skip = True
            cls.browser = None

    @classmethod
    def tearDownClass(cls):
        try:
            if cls.browser:
                cls.browser.quit()
        finally:
            super().tearDownClass()

    def setUp(self):
        if getattr(self, "_skip", False):
            self.skipTest("Chrome/driver tidak tersedia — melewatkan Selenium functional tests.")
        self.test_user = User.objects.create_user(username="testadmin", password="testpassword")

    def tearDown(self):
        if getattr(self, "_skip", False) or not self.browser:
            return
        try:
            self.browser.delete_all_cookies()
            self.browser.execute_script("window.localStorage.clear();")
            self.browser.execute_script("window.sessionStorage.clear();")
            self.browser.get("about:blank")
        except Exception:
            pass

    # ----- Helper -----
    def login_user(self):
        self.browser.get(f"{self.live_server_url}/login/")
        username_input = self.browser.find_element(By.NAME, "username")
        password_input = self.browser.find_element(By.NAME, "password")
        username_input.send_keys("testadmin")
        password_input.send_keys("testpassword")
        password_input.submit()

    # ----- Tests (functional) -----

    def test_login_page(self):
        self.login_user()
        wait = WebDriverWait(self.browser, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertIn(h1_element.text, ["Football News", "News", "Garuda Lounge News"])
        candidates = self.browser.find_elements(By.PARTIAL_LINK_TEXT, "Logout") + \
                     self.browser.find_elements(By.XPATH, "//button[contains(., 'Logout')]")
        self.assertTrue(len(candidates) >= 1)

    def test_register_page(self):
        self.browser.get(f"{self.live_server_url}/register/")
        h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertIn(h1_element.text, ["Register", "Sign Up", "Daftar"])
        username_input = self.browser.find_element(By.NAME, "username")
        password1_input = self.browser.find_element(By.NAME, "password1")
        password2_input = self.browser.find_element(By.NAME, "password2")
        username_input.send_keys("newuser")
        password1_input.send_keys("complexpass123")
        password2_input.send_keys("complexpass123")
        password2_input.submit()
        wait = WebDriverWait(self.browser, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        login_h1 = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertIn(login_h1.text, ["Login", "Sign In", "Masuk"])

    def test_create_news(self):
        self.login_user()
        add_btn = (self.browser.find_elements(By.PARTIAL_LINK_TEXT, "Add News")
                   or self.browser.find_elements(By.XPATH, "//button[contains(., 'Add News')]"))[0]
        add_btn.click()
        title_input = self.browser.find_element(By.NAME, "title")
        content_input = self.browser.find_element(By.NAME, "content")
        category_select = self.browser.find_element(By.NAME, "category")
        thumbnail_input = self.browser.find_element(By.NAME, "thumbnail")
        is_featured_checkbox = self.browser.find_element(By.NAME, "is_featured")

        title_input.send_keys("Test News Title")
        content_input.send_keys("Test news content for selenium testing")
        thumbnail_input.send_keys("https://example.com/image.jpg")
        Select(category_select).select_by_value("match")  # sesuaikan bila choices beda
        if not is_featured_checkbox.is_selected():
            is_featured_checkbox.click()

        title_input.submit()

        wait = WebDriverWait(self.browser, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertIn(h1_element.text, ["Football News", "News", "Garuda Lounge News"])
        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Test News Title")))
        self.assertTrue(self.browser.find_element(By.PARTIAL_LINK_TEXT, "Test News Title").is_displayed())

    def test_news_detail(self):
        self.login_user()
        news = News.objects.create(
            title="Detail Test News",
            content="Content for detail testing",
            user=self.test_user,
            category=getattr(News, "category", "update") if hasattr(News, "category") else "update",
        )
        self.browser.get(f"{self.live_server_url}/news/{news.id}/")
        page = self.browser.page_source
        self.assertIn("Detail Test News", page)
        self.assertIn("Content for detail testing", page)

    def test_logout(self):
        self.login_user()
        btns = self.browser.find_elements(By.XPATH, "//button[contains(., 'Logout')]")
        if btns:
            btns[0].click()
        else:
            self.browser.find_element(By.PARTIAL_LINK_TEXT, "Logout").click()
        wait = WebDriverWait(self.browser, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        h1_element = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertIn(h1_element.text, ["Login", "Sign In", "Masuk"])

    def test_filter_main_page(self):
        News.objects.create(title="My Test News", content="My news content", user=self.test_user, category="update")
        News.objects.create(title="Other User News", content="Other content", user=self.test_user, category="update")

        self.login_user()
        wait = WebDriverWait(self.browser, 20)

        (self.browser.find_elements(By.PARTIAL_LINK_TEXT, "All Articles")
         or self.browser.find_elements(By.XPATH, "//button[contains(., 'All Articles')]"))[0].click()
        wait.until(lambda d: "My Test News" in d.page_source and "Other User News" in d.page_source)
        self.assertIn("My Test News", self.browser.page_source)
        self.assertIn("Other User News", self.browser.page_source)

        (self.browser.find_elements(By.PARTIAL_LINK_TEXT, "My Articles")
         or self.browser.find_elements(By.XPATH, "//button[contains(., 'My Articles')]"))[0].click()
        wait.until(lambda d: "My Test News" in d.page_source)
        self.assertIn("My Test News", self.browser.page_source)
