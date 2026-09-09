from django.shortcuts import render
from main.models import Experience

def show_main(request):
    context = {
        "name": "Sultoni Rico Sabillilah",
        "npm": "2506657365",
        "study_program": "S1 Sistem Informasi",
        "bio": "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik pada pengembangan perangkat lunak dan analisis data.",
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name": "Sultoni Rico Sabillilah",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
