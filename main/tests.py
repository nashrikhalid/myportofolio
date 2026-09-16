from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import Experience

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            started_at=timezone.now()
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_experience_page_template_and_status(self):
        # 1. URL dapat diakses dan menggunakan template yang tepat.
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experiences.html")

    def test_experience_model_data_shown(self):
        # 2. Data model muncul di halaman HTML ketika ada data.
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, self.experience.title)
        self.assertContains(response, "Membantu mahasiswa memahami pengembangan web.")
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Present")

    def test_empty_experience_page(self):
        # 3. Halaman HTML menampilkan pesan kondisi kosong ketika belum ada data.
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_create_project_with_valid_password(self):
        # Berhasil menambahkan proyek jika password cocok
        response = self.client.post(reverse("main:create_project"), {
            "title": "Proyek Rahasia",
            "description": "Deskripsi proyek",
            "tech_stack": "Django",
            "password": "rahasia123",
        })
        self.assertEqual(response.status_code, 302)
        from main.models import Project
        self.assertTrue(Project.objects.filter(title="Proyek Rahasia").exists())

    def test_create_project_with_invalid_password(self):
        # Gagal menambahkan proyek jika password salah
        response = self.client.post(reverse("main:create_project"), {
            "title": "Proyek Hack",
            "description": "Deskripsi proyek",
            "tech_stack": "Django",
            "password": "passwordsalah",
        })
        self.assertEqual(response.status_code, 200)
        from main.models import Project
        self.assertFalse(Project.objects.filter(title="Proyek Hack").exists())
        self.assertContains(response, "Kode rahasia atau password salah!")

    def test_create_project_with_secret_header(self):
        # Berhasil menambahkan proyek jika request menyertakan header rahasia
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Proyek Header",
                "description": "Deskripsi proyek",
                "tech_stack": "Django",
            },
            HTTP_X_SECRET_KEY="rahasia123",
        )
        self.assertEqual(response.status_code, 302)
        from main.models import Project
        self.assertTrue(Project.objects.filter(title="Proyek Header").exists())

    def test_delete_project_with_valid_password(self):
        # Berhasil menghapus proyek jika password cocok
        from main.models import Project
        project = Project.objects.create(title="Proyek Untuk Dihapus")
        response = self.client.post(
            reverse("main:delete_project", args=[project.id]),
            {"password": "rahasia123"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(id=project.id).exists())

    def test_delete_project_with_invalid_password(self):
        # Gagal menghapus proyek jika password salah
        from main.models import Project
        project = Project.objects.create(title="Proyek Aman")
        response = self.client.post(
            reverse("main:delete_project", args=[project.id]),
            {"password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(id=project.id).exists())

    def test_delete_project_with_secret_header(self):
        # Berhasil menghapus proyek jika request menyertakan header rahasia
        from main.models import Project
        project = Project.objects.create(title="Proyek Header Delete")
        response = self.client.post(
            reverse("main:delete_project", args=[project.id]),
            HTTP_X_SECRET_KEY="rahasia123"
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(id=project.id).exists())

