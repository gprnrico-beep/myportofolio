from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from main.models import Experience, Project
from main.forms import ProjectForm, ExperienceForm

def show_main(request):
    context = {
        "name": "Sultoni Rico Sabillilah",
        "npm": "2506657365",
        "study_program": "S1 Sistem Informasi",
        "bio": "Mahasiswa Sistem Informasi Universitas Indonesia...",
    }
    return render(request, "index.html", context)

# Tambahkan 's' di nama fungsi agar sesuai dengan import di urls.py
def get_experiences_json(request):
    experience = Experience.objects.all()
    experience_json = serializers.serialize("json", experience)
    return HttpResponse(experience_json, content_type="application/json")

def show_experience(request):
    json_response = get_experiences_json(request)
    # Gunakan nama variabel 'deserialized_data', bukan 'ExperienceForm'
    deserialized_data = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience_list = [exp.object for exp in deserialized_data]
    
    context = {
        "name": "Sultoni Rico Sabillilah",
        "experience_list": experience_list,
    }
    return render(request, "experience.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        # Perbaiki typo: messages.success (dengan 's')
        messages.success(request, "Pengalaman baru berhasil ditambahkan")
        return redirect("main:show_experience")

    context = {
        "name": "Sultoni Rico Sabillilah",
        "form": form,
        "title_page": "Tambah Pengalaman",
    }
    return render(request, "experience_form.html", context)

def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        # Perbaiki typo: messages.success (dengan 's')
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")
        
    context = {
        "name": "Sultoni Rico Sabillilah",
        "form": form,
        "title_page": "Edit Pengalaman",
    }
    return render(request, "experience_form.html", context)

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")
    return redirect("main:show_experience")

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)
    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def show_projects(request):
    json_response = get_projects_json(request)
    deserialized_projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in deserialized_projects]
    title_query = request.GET.get("title", "").strip()
    context = {
        "name": "Sultoni Rico Sabillilah",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")
    
    context = {
        "name": "Sultoni Rico Sabillilah",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")
    return redirect("main:show_projects")