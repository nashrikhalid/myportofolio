from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Skill


class SkillAPITest(APITestCase):
    def setUp(self):
        self.skill = Skill.objects.create(name="Python", logo="fa-python")
        self.list_url = reverse("api:skill-list")
        self.detail_url = reverse("api:skill-detail", args=[self.skill.pk])
        self.payload = {"name": "SQL", "logo": "fa-database"}

    def test_public_search_and_detail(self):
        row = self.client.get(self.detail_url).json()
        self.assertEqual(set(row), {"id", "name", "logo"})
        self.assertEqual(self.client.get(self.list_url, {"name": "PYT"}).json(), [row])
        self.assertEqual(self.client.get(self.list_url, {"name": "unknown"}).json(), [])
        self.assertEqual(self.client.get(self.detail_url + "star/").status_code, 404)

    def test_readers_cannot_write(self):
        for user in (None, User.objects.create_user("member")):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"name": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
            self.skill.refresh_from_db()
            self.assertEqual(self.skill.name, "Python")
            self.assertEqual(Skill.objects.count(), 1)

    def test_editor_session_and_validation(self):
        user = User.objects.create_user("editor", password="test-password")
        user.groups.add(Group.objects.create(name="Editor"))
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="editor", password="test-password"))
        form = client.get(reverse("main:update_skill", args=[self.skill.pk]))
        self.assertContains(form, self.detail_url)
        self.assertEqual(client.put(self.detail_url, self.payload, format="json").status_code, 403)
        client.credentials(HTTP_X_CSRFTOKEN=client.cookies["csrftoken"].value)
        self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(client.delete(self.detail_url).status_code, 403)
        self.assertEqual(client.put(self.detail_url, self.payload, format="json").status_code, 200)
        self.assertEqual(client.patch(self.detail_url, {"name": "<b></b>"}, format="json").status_code, 400)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "SQL")

    def test_owner_create_and_delete(self):
        self.client.force_authenticate(User.objects.create_user("owner", is_superuser=True))
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        url = reverse("api:skill-detail", args=[response.data["id"]])
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertEqual(self.client.get(url).status_code, 404)
