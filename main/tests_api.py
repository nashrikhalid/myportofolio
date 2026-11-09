import uuid
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from main.models import Project, Experience
class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": 
"Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }
    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, 
status.HTTP_200_OK)
    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])
    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, 
status.HTTP_404_NOT_FOUND)
    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, 
format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": 
"Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")
    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())
    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, { **self.payload, 
**changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)
    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, 
format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, 
format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())
    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 
status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)
    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, 
format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, 
status.HTTP_405_METHOD_NOT_ALLOWED)
    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)
    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.obj = Experience.objects.create(title='Research', org='UI', description='Study')
        self.url = reverse('api:experience-detail', args=[self.obj.pk])
        self.list_url = reverse('api:experience-list')
        self.payload = {
            'title': 'Work', 'org': 'Fakultas Ilmu Komputer', 'description': 'Study',
            'category': 'research', 'started_at': '2026-11', 'ended_at': None,
        }
        self.editor = User.objects.create_user('editor')
        self.editor.groups.add(Group.objects.create(name='Editor'))

    def test_editor_update_but_not_create_delete(self):
        self.client.force_authenticate(self.editor)
        self.assertEqual(self.client.patch(self.url, {'title': 'Updated'}, format='json').status_code, 200)
        self.assertEqual(self.client.post(self.list_url, self.payload, format='json').status_code, 403)
        self.assertEqual(self.client.delete(self.url).status_code, 403)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.title, 'Updated')
        self.assertEqual(Experience.objects.count(), 1)

    def test_public_read_and_member_denied(self):
        self.assertEqual(self.client.get(self.list_url).status_code, 200)
        self.assertEqual(self.client.get(self.url).status_code, 200)
        member = User.objects.create_user('member')
        for user in (None, member):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format='json').status_code, 403)
            self.assertEqual(self.client.put(self.url, self.payload, format='json').status_code, 403)
            self.assertEqual(self.client.patch(self.url, {'org': 'Changed'}, format='json').status_code, 403)
            self.assertEqual(self.client.delete(self.url).status_code, 403)
            self.assertEqual(Experience.objects.count(), 1)
            self.obj.refresh_from_db()
            self.assertEqual(self.obj.org, 'UI')

    def test_star_requires_login_and_toggles(self):
        star = reverse('api:experience-star', args=[self.obj.pk])
        self.assertEqual(self.client.post(star).status_code, 403)
        self.assertEqual(self.obj.starred_by.count(), 0)
        member = User.objects.create_user('member')
        self.client.force_authenticate(member)
        for expected in (True, False):
            response = self.client.post(star)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['is_starred'], expected)
            self.assertEqual(self.obj.starred_by.filter(pk=member.pk).exists(), expected)

    def test_editor_edit_form_with_session_requires_csrf(self):
        self.editor.set_password('editor-test-password')
        self.editor.save()
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username='editor', password='editor-test-password'))
        page = client.get(reverse('main:update_experience', args=[self.obj.pk]))
        self.assertContains(page, f'data-edit-url="{self.url}"')
        response = client.put(self.url, self.payload, format='json')
        self.assertEqual(response.status_code, 403)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.org, 'UI')
        token = client.cookies['csrftoken'].value
        response = client.put(self.url, self.payload, format='json', HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 200)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.org, self.payload['org'])
        self.assertIsNone(self.obj.ended_at)

    def test_owner_month_input_and_validation(self):
        owner = User.objects.create_superuser('owner', email='owner@example.com', password='test')
        self.client.force_authenticate(owner)
        response = self.client.post(self.list_url, self.payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['is_ongoing'])
        self.assertEqual(self.client.patch(self.url, {'org': '<b></b>'}, format='json').status_code, 400)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.org, 'UI')
        self.assertEqual(self.client.delete(self.url).status_code, 204)
        self.assertFalse(Experience.objects.filter(pk=self.obj.pk).exists())
