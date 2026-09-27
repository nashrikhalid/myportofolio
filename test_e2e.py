"""Tutorial 4 browser tests. Run directly; uses a temporary Django test database."""
import argparse
import os
from pathlib import Path
import sys
import unittest

from dotenv import load_dotenv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--burp", action="store_true", help="Use localhost:8080; manually remove CSRF in Burp when prompted")
    args = parser.parse_args()
    load_dotenv(Path(__file__).with_name(".env"))
    if os.getenv("PRODUCTION", "False").lower() == "true":
        parser.error("Pengujian ini hanya untuk database lokal, bukan PWS.")
    passwords = [os.getenv("E2E_USER_PASSWORD"), os.getenv("E2E_ADMIN_PASSWORD")]
    if not all(passwords):
        parser.error("Isi E2E_USER_PASSWORD dan E2E_ADMIN_PASSWORD di .env terlebih dahulu.")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portofolio.settings")
    import django
    django.setup()
    from django.conf import settings
    from django.contrib.auth.models import User
    from django.contrib.staticfiles.testing import StaticLiveServerTestCase
    from django.test.runner import DiscoverRunner
    from main.models import Project
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    if settings.DATABASES["default"]["ENGINE"] != "django.db.backends.sqlite3":
        parser.error("Pengujian dibatasi ke SQLite lokal.")
    evidence = Path("artifacts/tutorial4")
    evidence.mkdir(parents=True, exist_ok=True)

    class BrowserTutorialTest(StaticLiveServerTestCase):
        host = "127.0.0.1"

        def test_tutorial_flow(self):
            User.objects.create_user("visitor_e2e", password=passwords[0])
            User.objects.create_superuser("owner_e2e", password=passwords[1])
            options = webdriver.ChromeOptions()
            if args.headless:
                options.add_argument("--headless=new")
            options.add_argument("--window-size=1440,1000")
            if args.burp:
                options.add_argument("--proxy-server=http://127.0.0.1:8080")
                options.add_argument("--proxy-bypass-list=<-loopback>")
            driver = webdriver.Chrome(options=options)
            self.addCleanup(driver.quit)
            driver.set_page_load_timeout(360 if args.burp else 30)
            wait = WebDriverWait(driver, 20)
            base = self.live_server_url

            def login(username, password):
                driver.get(base + "/login/")
                wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
                driver.find_element(By.NAME, "password").send_keys(password)
                driver.find_element(By.CSS_SELECTOR, ".project-form button[type=submit]").click()
                wait.until(EC.url_to_be(base + "/"))
                wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "nav-user"), username))

            driver.get(base + "/login/")
            self.assertTrue(driver.find_element(By.NAME, "csrfmiddlewaretoken").get_attribute("value"))
            self.assertTrue(driver.get_cookie("csrftoken"))
            print("[PASS] Hidden input CSRF dan cookie csrftoken tersedia", flush=True)
            login("visitor_e2e", passwords[0])
            self.assertTrue(driver.get_cookie("sessionid"))
            self.assertTrue(driver.get_cookie("last_login"))
            self.assertIn("Sesi Terakhir Login", driver.page_source)
            driver.save_screenshot(str(evidence / "01-login.png"))
            print("[PASS] Login, sessionid, last_login, dan navbar", flush=True)
            driver.get(base + "/experience/")
            self.assertEqual(driver.find_element(By.CLASS_NAME, "nav-user").text, "visitor_e2e")
            driver.get(base + "/projects/add/")
            self.assertIn("Forbidden", driver.page_source)
            driver.save_screenshot(str(evidence / "02-forbidden.png"))
            print("[PASS] Session lintas halaman; akun biasa ditolak dari tambah proyek", flush=True)
            driver.get(base + "/logout/")
            login("owner_e2e", passwords[1])
            driver.get(base + "/projects/add/")
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "project-form")))
            print("[PASS] Superuser dapat membuka form tambah proyek", flush=True)

            driver.find_element(By.NAME, "title").clear()
            driver.find_element(By.NAME, "description").clear()
            if args.burp:
                driver.find_element(By.NAME, "title").send_keys("Burp CSRF blocked")
                driver.find_element(By.NAME, "description").send_keys("Request ini harus ditolak dan tidak tersimpan.")
                print("[BURP READY] Aktifkan Intercept sekarang, lalu tekan Enter di terminal ini.", flush=True)
                input()
                print("[BURP] Hapus nilai csrfmiddlewaretoken, lalu Forward. Batas waktu 6 menit.", flush=True)
                driver.find_element(By.CSS_SELECTOR, ".project-form button[type=submit]").click()
                WebDriverWait(driver, 360).until(lambda d: "CSRF verification failed" in d.page_source)
                self.assertIn("403", driver.title)
                self.assertEqual(Project.objects.count(), 0)
                driver.save_screenshot(str(evidence / "03-burp-csrf.png"))
                print("[PASS] Burp: token dihapus, respons 403, database tidak berubah", flush=True)
                print("[BURP] Matikan Intercept, lalu tekan Enter untuk logout.", flush=True)
                input()
            else:
                # Companion check, not a substitute for an actual Burp interception.
                driver.find_element(By.NAME, "title").send_keys("Selenium CSRF blocked")
                driver.find_element(By.NAME, "description").send_keys("Missing CSRF test")
                driver.execute_script("document.querySelector('[name=csrfmiddlewaretoken]').remove()")
                driver.find_element(By.CSS_SELECTOR, ".project-form button[type=submit]").click()
                wait.until(lambda d: "CSRF verification failed" in d.page_source)
                self.assertEqual(Project.objects.count(), 0)
                driver.save_screenshot(str(evidence / "03-selenium-csrf.png"))
                print("[PASS] Selenium: POST tanpa token CSRF ditolak", flush=True)

            driver.get(base + "/logout/")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "nav a[href='/login/']")))
            self.assertFalse(driver.get_cookie("sessionid"))
            self.assertFalse(driver.get_cookie("last_login"))
            print("[PASS] Logout menghapus sessionid dan last_login", flush=True)

    runner = DiscoverRunner(verbosity=2, interactive=False)
    runner.setup_test_environment()
    old_config = None
    try:
        old_config = runner.setup_databases()
        result = runner.run_suite(unittest.defaultTestLoader.loadTestsFromTestCase(BrowserTutorialTest))
        return 0 if result.wasSuccessful() else 1
    finally:
        if old_config is not None:
            runner.teardown_databases(old_config)
        runner.teardown_test_environment()


if __name__ == "__main__":
    sys.exit(main())
