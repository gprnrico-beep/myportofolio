from django.test import TestCase, Client
from django.urls import reverse
from main.models import Experience, Project

class MainAppTests(TestCase):
    def setUp(self):
        self.client = Client()

    # Test 1: Verifikasi rute utama (Profile)
    def test_main_page_status_and_template(self):
        response = self.client.get(reverse('main:show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    # Test 2: Verifikasi rute Experience dan pemanggilan datanya
    def test_experience_page_and_content(self):
        Experience.objects.create(
            title="Uji Pengalaman",
            description="Deskripsi uji coba untuk unit test."
        )
        response = self.client.get(reverse('main:show_experience'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'experience.html')
        self.assertContains(response, "Uji Pengalaman")

    # Test 3: Verifikasi rute Projects dan pemanggilan datanya
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