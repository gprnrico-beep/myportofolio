
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project


class ProjectAPITestCase(APITestCase):

    def setUp(self):
        # Membuat pengguna untuk pengujian
        self.superuser = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='testpassword123'
        )

        self.editor = User.objects.create_user(
            username='editor_test',
            password='testpassword123'
        )

        self.regular_user = User.objects.create_user(
            username='user_test',
            password='testpassword123'
        )

        # Membuat grup Editor
        self.editor_group = Group.objects.create(name='Editor')
        self.editor.groups.add(self.editor_group)

        # Membuat data project
        self.project = Project.objects.create(
            title='Portfolio Website',
            category='Web Development',
            description='A personal portfolio website.'
        )

        self.project_url = (
            f'/api/v1/projects/{self.project.id}/'
        )

        self.list_url = '/api/v1/projects/'

    # 1. Semua pengguna dapat melihat daftar project
    def test_list_projects(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 1)

    # 2. Semua pengguna dapat melihat detail project
    def test_project_detail(self):
        response = self.client.get(self.project_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['title'],
            'Portfolio Website'
        )

    # 3. Pengguna dapat mencari project berdasarkan judul
    def test_search_projects_by_title(self):
        response = self.client.get(
            self.list_url,
            {'title': 'Portfolio'}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 1)

    # 4. Pengguna tanpa login tidak dapat membuat project
    def test_unauthenticated_user_cannot_create_project(self):
        response = self.client.post(
            self.list_url,
            {
                'title': 'New Project',
                'category': 'Web',
                'description': 'New project description.'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    # 5. Superuser dapat membuat project
    def test_superuser_can_create_project(self):
        self.client.force_authenticate(user=self.superuser)

        response = self.client.post(
            self.list_url,
            {
                'title': 'New Project',
                'category': 'Web',
                'description': 'New project description.'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(Project.objects.count(), 2)

    # 6. Pengguna biasa tidak dapat mengubah project
    def test_regular_user_cannot_update_project(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.patch(
            self.project_url,
            {'title': 'Updated Title'},
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    # 7. Editor dapat memperbarui project menggunakan PUT
    def test_editor_can_update_project_with_put(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.put(
            self.project_url,
            {
                'title': 'Updated Portfolio',
                'category': 'Web Development',
                'description': 'Updated description.'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['title'],
            'Updated Portfolio'
        )

    # 8. Editor dapat memperbarui sebagian data menggunakan PATCH
    def test_editor_can_update_project_with_patch(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(
            self.project_url,
            {'title': 'Patched Portfolio'},
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['title'],
            'Patched Portfolio'
        )

    # 9. Editor tidak dapat menghapus project
    def test_editor_cannot_delete_project(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.delete(self.project_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    # 10. Superuser dapat menghapus project
    def test_superuser_can_delete_project(self):
        self.client.force_authenticate(user=self.superuser)

        response = self.client.delete(self.project_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(Project.objects.count(), 0)

    # 11. Pengguna tanpa login tidak dapat memberikan star
    def test_unauthenticated_user_cannot_star_project(self):
        response = self.client.post(
            f'{self.project_url}star/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    # 12. Pengguna yang login dapat menambah dan menghapus star
    def test_authenticated_user_can_toggle_star(self):
        self.client.force_authenticate(user=self.regular_user)

        # Menambahkan star
        response = self.client.post(
            f'{self.project_url}star/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertTrue(
            self.project.starred_by.filter(
                pk=self.regular_user.pk
            ).exists()
        )

        # Menghapus star
        response = self.client.post(
            f'{self.project_url}star/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertFalse(
            self.project.starred_by.filter(
                pk=self.regular_user.pk
            ).exists()
        )

    # 13. Detail project yang tidak ditemukan menghasilkan 404
    def test_project_not_found(self):
        response = self.client.get(
            '/api/v1/projects/00000000-0000-0000-0000-000000000000/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
