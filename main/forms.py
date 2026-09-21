from django.forms import ModelForm, TextInput, Textarea, Select
from main.models import Experience, Project

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "category",
            "description",
        ]
        labels = {
            "title": "Judul Pengalaman",
            "category": "Kategori",
            "description": "Deskripsi Pengalaman",
        }
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "misal: Staff SOSPRO",
                    "maxlength": 255,
                }
            ),
            "category": Select(
                choices=Experience.EXPERIENCE_CHOICES,
                attrs={
                    "class": "form-control",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Saya berperan di divisi logistik...",
                    "rows": 4,
                }
            ),
        }

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "category",
            "description",
        ]
        labels = {
            "title": "Judul Proyek",
            "category": "Kategori",
            "description": "Deskripsi Proyek",
        }
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "misal: Aplikasi Web NuMate",
                    "maxlength": 255,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "misal: Web Development",
                    "maxlength": 100,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Deskripsi singkat mengenai proyek...",
                    "rows": 4,
                }
            ),
        }