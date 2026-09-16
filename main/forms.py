from django.forms import ModelForm, TextInput, Textarea
from main.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "category",
            "description",
        ]
        labels = {
            "title": "Nama Proyek",
            "category": "Kategori Proyek",
            "description": "Deskripsi Proyek",
        }
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "misal: NuMate - AI Grocery App",
                    "maxlength": 255,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "misal: Web Development / Machine Learning",
                    "maxlength": 100,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Jelaskan proyek yang kamu buat...",
                    "rows": 4,
                }
            ),
        }