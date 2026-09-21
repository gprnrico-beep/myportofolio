from django.test import TestCase, Client
from django.urls import reverse
from main.models import Experience, Project

class MainAppTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_main_page_status_and_template(self):
        response = self.client.get(reverse('main:show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_experience_page_and_content(self):
        Experience.objects.create(
            title="Uji Pengalaman",
            category="internship",  # Opsi valid
            description="Deskripsi uji coba untuk unit test."
        )
        response = self.client.get(reverse('main:show_experience'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'experience.html')
        self.assertContains(response, "Uji Pengalaman")

    def test_projects_page_and_content(self):
        Project.objects.create(
            title="Uji Proyek",
            category="Test Category",
            description="Deskripsi uji coba proyek."
        )
        response = self.client.get(reverse('main:show_projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects.html')
        self.assertContains(response, "Uji Proyek")

    def test_get_experiences_json(self):
        Experience.objects.create(
            title="API Test Experience",
            category="volunteer",  # Mengubah 'WORK' -> 'volunteer' (opsi valid)
            description="Test API JSON"
        )
        response = self.client.get(reverse('main:get_experiences_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertContains(response, "API Test Experience")

    def test_get_projects_json(self):
        Project.objects.create(
            title="API Test Project",
            category="Web",
            description="Tes API JSON Proyek"
        )
        response = self.client.get(reverse('main:get_projects_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertContains(response, "API Test Project")

    def test_create_experience_post(self):
        response = self.client.post(reverse('main:create_experience'), {
            'title': 'Pengalaman Baru via POST',
            'category': 'internship',  # Mengubah 'ORGANIZATION' -> 'internship' (opsi valid)
            'description': 'Deskripsi via POST form'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Experience.objects.filter(title='Pengalaman Baru via POST').exists())