from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import Experience
from main.models import Project
from django.contrib.auth.models import Group, User
from django.test import Client
from main.models import Skill


class SkillDeleteTest(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(name="Python", logo="fa-brands fa-python")
        self.url = reverse("main:delete_skill", args=[self.skill.pk])
        self.owner = User.objects.create_user("skill_owner", is_superuser=True)
        self.visitor = User.objects.create_user("skill_visitor")

    def test_delete_requires_superuser_even_with_secret(self):
        response = self.client.post(self.url, {"password": "rahasia123"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("main:login") + "?next="))
        self.client.force_login(self.visitor)
        for method in (self.client.get, self.client.post):
            self.assertEqual(method(self.url, HTTP_X_SECRET_KEY="rahasia123").status_code, 403)
        self.assertTrue(Skill.objects.filter(pk=self.skill.pk).exists())

    def test_owner_get_preserves_skill_and_post_deletes_it(self):
        self.client.force_login(self.owner)
        self.client.get(self.url)
        self.assertTrue(Skill.objects.filter(pk=self.skill.pk).exists())
        response = self.client.post(self.url)
        self.assertRedirects(response, "/#skills", fetch_redirect_response=False)
        self.assertFalse(Skill.objects.filter(pk=self.skill.pk).exists())
        self.assertContains(self.client.get(reverse("main:show_main")), "Skill berhasil dihapus!")

    def test_delete_controls_only_visible_to_owner(self):
        marker = 'popovertarget="delete-skill-' + str(self.skill.pk) + '"'
        for page in ("main:show_main", "main:show_skill"):
            self.client.logout()
            self.assertNotContains(self.client.get(reverse(page)), marker)
            self.client.force_login(self.visitor)
            self.assertNotContains(self.client.get(reverse(page)), marker)
            self.client.force_login(self.owner)
            response = self.client.get(reverse(page))
            self.assertContains(response, marker)
            self.assertContains(response, 'action="' + self.url + '"')

    def test_delete_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        client.get(reverse("main:show_main"))
        self.assertEqual(client.post(self.url).status_code, 403)
        self.assertTrue(Skill.objects.filter(pk=self.skill.pk).exists())
        response = client.post(self.url, {"csrfmiddlewaretoken": client.cookies["csrftoken"].value})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Skill.objects.filter(pk=self.skill.pk).exists())

class AssignmentFourTest(TestCase):
    """Kontrak Tugas 4; akun dan objek hanya hidup di database pengujian."""

    @classmethod
    def setUpTestData(cls):
        cls.member = User.objects.create_user("assignment_member", email="private@example.com")
        cls.editor = User.objects.create_user("assignment_editor")
        cls.owner = User.objects.create_user("assignment_owner", is_superuser=True)
        cls.editor.groups.add(Group.objects.create(name="Editor"))
        cls.project = Project.objects.create(title="Original project", description="Original")
        cls.experience = Experience.objects.create(title="Original experience", org="UI", description="Original")
        cls.skill = Skill.objects.create(name="Original skill", logo="fa-python")

    def resources(self):
        return [
            ("project", self.project, {"title": "Changed project", "description": "Updated"}),
            ("experience", self.experience, {"title": "Changed experience", "org": "UI", "description": "Updated", "category": "research", "started_at": "2026-09-01", "ended_at": ""}),
            ("skill", self.skill, {"name": "Changed skill", "logo": "fa-python"}),
        ]

    def test_anonymous_mutations_redirect_to_login(self):
        for name, obj, data in self.resources():
            for action in ("create", "update", "delete"):
                url = reverse(f"main:{action}_{name}", args=[] if action == "create" else [obj.pk])
                for method in (self.client.get, self.client.post):
                    with self.subTest(resource=name, action=action, method=method.__name__):
                        response = method(url) if method.__name__ == "get" else method(url, data)
                        self.assertRedirects(response, reverse("main:login") + "?next=" + url, fetch_redirect_response=False)
        url = reverse("main:toggle_experience_star", args=[self.experience.pk])
        self.assertRedirects(self.client.post(url), reverse("main:login") + "?next=" + url, fetch_redirect_response=False)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_member_cannot_write_and_editor_cannot_create_or_delete(self):
        for user, actions in [(self.member, ("create", "update", "delete")), (self.editor, ("create", "delete"))]:
            self.client.force_login(user)
            for name, obj, data in self.resources():
                original = type(obj).objects.values().get(pk=obj.pk)
                for action in actions:
                    url = reverse(f"main:{action}_{name}", args=[] if action == "create" else [obj.pk])
                    for method in (self.client.get, self.client.post):
                        with self.subTest(role=user.username, resource=name, action=action, method=method.__name__):
                            self.assertEqual(method(url, data).status_code, 403)
                            self.assertEqual(type(obj).objects.count(), 1)
                            self.assertEqual(type(obj).objects.values().get(pk=obj.pk), original)

    def test_editor_and_owner_can_save_edits_without_secret(self):
        for user in (self.editor, self.owner):
            self.client.force_login(user)
            for name, obj, data in self.resources():
                with self.subTest(role=user.username, resource=name):
                    url = reverse(f"main:update_{name}", args=[obj.pk])
                    self.assertEqual(self.client.get(url).status_code, 200)
                    self.assertEqual(self.client.post(url, data).status_code, 302)
                    obj.refresh_from_db()
                    field = "name" if name == "skill" else "title"
                    self.assertEqual(getattr(obj, field), data[field])

    def test_owner_can_create_and_delete_without_secret(self):
        self.client.force_login(self.owner)
        for name, obj, data in self.resources():
            with self.subTest(resource=name):
                response = self.client.post(reverse(f"main:create_{name}"), data)
                self.assertEqual(response.status_code, 302)
                created = type(obj).objects.exclude(pk=obj.pk).get()
                url = reverse(f"main:delete_{name}", args=[created.pk])
                self.client.get(url)
                self.assertTrue(type(obj).objects.filter(pk=created.pk).exists())
                self.assertEqual(self.client.post(url).status_code, 302)
                self.assertFalse(type(obj).objects.filter(pk=created.pk).exists())

    def test_controls_match_roles_on_all_pages(self):
        pages = [("show_project", "project", self.project), ("show_experience", "experience", self.experience), ("show_skill", "skill", self.skill), ("show_main", "skill", self.skill)]
        for user in (None, self.member, self.editor, self.owner):
            self.client.logout()
            if user:
                self.client.force_login(user)
            for page, name, obj in pages:
                with self.subTest(role=user.username if user else "anonymous", page=page):
                    response = self.client.get(reverse("main:" + page))
                    self.assertEqual(response.status_code, 200)
                    edit = reverse(f"main:update_{name}", args=[obj.pk])
                    (self.assertContains if user in (self.editor, self.owner) else self.assertNotContains)(response, edit)
                    for url in [reverse(f"main:create_{name}"), reverse(f"main:delete_{name}", args=[obj.pk])]:
                        (self.assertContains if user == self.owner else self.assertNotContains)(response, url)

    def test_experience_star_is_per_account_post_only_and_visible(self):
        url = reverse("main:toggle_experience_star", args=[self.experience.pk])
        for user in (self.member, self.editor, self.owner):
            self.client.force_login(user)
            before = self.experience.starred_by.count()
            self.client.get(url)
            self.assertEqual(self.experience.starred_by.count(), before)
            self.assertRedirects(self.client.post(url), reverse("main:show_experience"))
            self.assertEqual(self.experience.starred_by.count(), before + 1)
            response = self.client.get(reverse("main:show_experience"))
            self.assertContains(response, "Unstar")
            self.assertContains(response, f'class="star-count">{before + 1}')
        self.experience.starred_by.add(self.member)
        self.assertEqual(self.experience.starred_by.count(), 3)
        self.client.force_login(self.member)
        self.client.post(url)
        self.assertEqual(self.experience.starred_by.count(), 2)
        self.assertFalse(self.experience.starred_by.filter(pk=self.member.pk).exists())

    def test_experience_star_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.member)
        client.get(reverse("main:show_experience"))
        url = reverse("main:toggle_experience_star", args=[self.experience.pk])
        self.assertEqual(client.post(url).status_code, 403)
        self.assertEqual(self.experience.starred_by.count(), 0)
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(url, {"csrfmiddlewaretoken": token}).status_code, 302)
        self.assertEqual(self.experience.starred_by.count(), 1)

    def test_public_json_fields_and_search(self):
        expected = {
            "projects": {"title", "description", "tech_stack", "project_url", "project_image_url", "starred_by"},
            "experiences": {"title", "org", "description", "category", "started_at", "ended_at", "starred_by"},
            "skills": {"name", "logo"},
        }
        for name, fields in expected.items():
            with self.subTest(endpoint=name):
                url = reverse(f"main:get_{name}_json")
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response["Content-Type"], "application/json")
                self.assertEqual(set(response.json()[0]["fields"]), fields)
                self.assertNotContains(response, self.member.email)
                key = "name" if name == "skills" else "title"
                self.assertEqual(len(self.client.get(url, {key: "Original"}).json()), 1)
                self.assertEqual(self.client.get(url, {key: "absent"}).json(), [])

    def test_star_json_uses_usernames_as_in_tutorial(self):
        for obj, endpoint in [(self.project, "get_projects_json"), (self.experience, "get_experiences_json")]:
            with self.subTest(endpoint=endpoint):
                obj.starred_by.add(self.member)
                data = self.client.get(reverse("main:" + endpoint)).json()
                self.assertEqual(data[0]["fields"]["starred_by"], [[self.member.username]])


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


class TutorialFourTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "Test-only-Password-2026!"
        cls.user = User.objects.create_user("visitor", password=cls.password)
        cls.other = User.objects.create_user("another", password=cls.password)
        cls.owner = User.objects.create_superuser("owner", password=cls.password)
        cls.project = Project.objects.create(title="Tutorial Project", description="Example")

    def test_public_pages_and_controls(self):
        for name in ["show_main", "show_project", "show_experience", "login", "register", "get_projects_json"]:
            self.assertEqual(self.client.get(reverse("main:" + name)).status_code, 200)
        response = self.client.get(reverse("main:show_project"))
        self.assertContains(response, "Star")
        self.assertNotContains(response, "Tambah Proyek")
        self.assertNotContains(response, "Hapus Proyek")
        self.assertNotContains(response, reverse("main:update_project", args=[self.project.pk]))
        self.client.force_login(self.owner)
        response = self.client.get(reverse("main:show_project"))
        for text in ["Tambah Proyek", "Hapus Proyek", reverse("main:update_project", args=[self.project.pk])]:
            self.assertContains(response, text)

    def test_register_validation_and_password_hash(self):
        url = reverse("main:register")
        for username, confirmation in [("visitor", self.password), ("newuser", "mismatch")]:
            response = self.client.post(url, {"username": username, "password1": self.password, "password2": confirmation})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["form"].errors)
        self.assertFalse(User.objects.filter(username="newuser").exists())
        response = self.client.post(url, {"username": "newuser", "password1": self.password, "password2": self.password}, follow=True)
        self.assertContains(response, "Akun berhasil dibuat. Silakan login.", count=1)
        user = User.objects.get(username="newuser")
        self.assertTrue(user.check_password(self.password))
        self.assertNotEqual(user.password, self.password)
        self.assertFalse(user.is_superuser)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_session_cookie_and_logout(self):
        url = reverse("main:login")
        response = self.client.post(url, {"username": "visitor", "password": "wrong"})
        self.assertTrue(response.context["form"].non_field_errors())
        self.assertNotIn("last_login", response.cookies)
        response = self.client.post(url, {"username": "visitor", "password": self.password})
        self.assertRedirects(response, reverse("main:show_main"))
        timestamp = response.cookies["last_login"].value
        self.assertRegex(timestamp, r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
        self.assertEqual(self.client.session["_auth_user_id"], str(self.user.pk))
        self.assertContains(self.client.get(reverse("main:show_main")), timestamp)
        self.assertContains(self.client.get(reverse("main:show_experience")), 'class="nav-user">visitor')
        response = self.client.get(reverse("main:logout"))
        self.assertEqual(response.cookies["last_login"]["max-age"], 0)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())
        self.assertContains(Client().get(reverse("main:show_main")), "Belum ada sesi login")

    def test_project_writes_require_owner_even_with_legacy_secret(self):
        urls = [reverse("main:create_project"), reverse("main:update_project", args=[self.project.pk]), reverse("main:delete_project", args=[self.project.pk])]
        for url in urls:
            for method in [self.client.get, self.client.post]:
                response = method(url, {"password": "rahasia123"}, HTTP_X_SECRET_KEY="rahasia123")
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("main:login") + "?next="))
        self.client.force_login(self.user)
        for url in urls:
            for method in [self.client.get, self.client.post]:
                self.assertEqual(method(url, {"password": "rahasia123"}, HTTP_X_SECRET_KEY="rahasia123").status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Tutorial Project")

    def test_owner_project_crud_without_secret(self):
        self.client.force_login(self.owner)
        url = reverse("main:create_project")
        self.assertNotContains(self.client.get(url), 'name="password"')
        self.assertEqual(self.client.post(url, {"title": ""}).status_code, 200)
        self.assertEqual(Project.objects.count(), 1)
        self.client.post(url, {"title": "New project", "description": "Created"})
        project = Project.objects.get(title="New project")
        edit_url = reverse("main:update_project", args=[project.pk])
        self.assertContains(self.client.get(edit_url), 'action="' + edit_url + '"')
        self.client.post(edit_url, {"title": "Edited project", "description": "Edited"})
        project.refresh_from_db()
        self.assertEqual(project.title, "Edited project")
        delete_url = reverse("main:delete_project", args=[project.pk])
        self.client.get(delete_url)
        self.assertTrue(Project.objects.filter(pk=project.pk).exists())
        self.client.post(delete_url)
        self.assertFalse(Project.objects.filter(pk=project.pk).exists())

    def test_stars_are_per_user_post_only_and_visible_in_api(self):
        url = reverse("main:toggle_project_star", args=[self.project.pk])
        self.assertEqual(self.client.post(url).status_code, 302)
        self.assertEqual(self.project.starred_by.count(), 0)
        self.client.force_login(self.user)
        self.client.get(url)
        self.assertEqual(self.project.starred_by.count(), 0)
        self.client.post(url)
        self.assertEqual(self.project.starred_by.count(), 1)
        response = self.client.get(reverse("main:show_project"))
        self.assertContains(response, "Unstar")
        self.assertContains(response, "Dibintangi oleh visitor")
        self.assertContains(response, 'class="star-count">1')
        self.assertNotContains(response, "Hapus Proyek")
        data = self.client.get(reverse("main:get_projects_json")).json()
        self.assertEqual(data[0]["fields"]["starred_by"], [["visitor"]])
        self.client.force_login(self.other)
        self.client.post(url)
        self.assertEqual(self.project.starred_by.count(), 2)
        self.client.force_login(self.user)
        self.client.post(url)
        self.assertEqual(list(self.project.starred_by.all()), [self.other])
        self.assertEqual(self.user.starred_projects.count(), 0)

    def test_project_search_and_missing_project(self):
        self.assertContains(self.client.get(reverse("main:show_project"), {"title": "Tutorial"}), self.project.title)
        self.assertNotContains(self.client.get(reverse("main:show_project"), {"title": "absent"}), self.project.title)
        self.client.force_login(self.user)
        self.assertEqual(self.client.post(reverse("main:toggle_project_star", args=["00000000-0000-0000-0000-000000000000"])).status_code, 404)

    def test_csrf_rejects_missing_token_and_accepts_form_or_header(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        create_url = reverse("main:create_project")
        response = client.get(create_url)
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertEqual(client.post(create_url, {"title": "Blocked", "description": "No token"}).status_code, 403)
        self.assertFalse(Project.objects.filter(title="Blocked").exists())
        token = client.cookies["csrftoken"].value
        response = client.post(create_url, {"title": "CSRF allowed", "description": "Valid", "csrfmiddlewaretoken": token})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(title="CSRF allowed").exists())
        star_url = reverse("main:toggle_project_star", args=[self.project.pk])
        self.assertEqual(client.post(star_url).status_code, 403)
        self.assertEqual(client.post(star_url, HTTP_X_CSRFTOKEN="invalid").status_code, 403)
        self.assertEqual(client.post(star_url, HTTP_X_CSRFTOKEN=token).status_code, 302)
        self.assertTrue(self.project.starred_by.filter(pk=self.owner.pk).exists())

