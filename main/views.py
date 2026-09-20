import os
from django.conf import settings
from django.shortcuts import render
from main.models import Experience
from main.models import Project
from main.models import Skill
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from main.forms import ProjectForm, ExperienceForm


def is_authorized(request):
    secret = getattr(settings, 'PORTFOLIO_SECRET', os.getenv('PORTFOLIO_SECRET', 'rahasia123'))

    # 1. Cek custom header pada request (misal: X-Secret-Key)
    header_secret = (
        request.headers.get("X-Secret-Key")
        or request.headers.get("X-Portfolio-Secret")
        or request.headers.get("X-Admin-Secret")
        or request.headers.get("Secret-Key")
        or request.META.get("HTTP_X_SECRET_KEY")
    )
    if header_secret and header_secret == secret:
        return True

    # 2. Cek field password pada form (POST)
    post_password = request.POST.get("password")
    if post_password and post_password == secret:
        return True

    return False


def show_main(request):
    context = {
        "name": "Nashri",
        "fullname": "Nashri Khalid",
        "npm": "2506657131",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Based in Jakarta, Nashri is a curious explorer who enjoys trying new things before settling on one path. "
            "His interests currently span product management, data analysis, and data engineering, though he stays "
            "open to wherever his curiosity leads next. He is currently on progress learning a variety of tools to"
            "sharpen his skills in these fields. Organizationally active since high school, he has developed"
            "cross-functional collaboration and decision-making abilities through various leadership and operational"
            "roles. Outside of academics, he loves music, especially singing, as a way to unwind and recharge."
        ),
        "skill_list": Skill.objects.all(),
    }
    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experiences_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [exp.object for exp in experiences]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Nashri",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experiences.html", context)

def show_project(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Nashri",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def show_skill(request):
    context = {
        "name": "Nashri",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skills.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST":
        if not is_authorized(request):
            form.add_error("password", "Kode rahasia atau password salah!")
            messages.error(request, "Akses ditolak: Password atau header rahasia salah!")
        elif form.is_valid():
            form.save()
            messages.success(request, "Proyek baru berhasil ditambahkan!")
            return redirect("main:show_project")

    context = {
        "name": "Nashri",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if not is_authorized(request):
            messages.error(request, "Akses ditolak: Kode rahasia atau password salah!")
            return redirect("main:show_project")

        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST":
        if not is_authorized(request):
            form.add_error("password", "Kode rahasia atau password salah!")
            messages.error(request, "Akses ditolak: Password atau header rahasia salah!")
        elif form.is_valid():
            form.save()
            messages.success(request, "Pengalaman baru berhasil ditambahkan!")
            return redirect("main:show_experience")

    context = {
        "name": "Nashri",
        "form": form,
    }
    return render(request, "experiences_form.html", context)

def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST":
        if not is_authorized(request):
            form.add_error("password", "Kode rahasia atau password salah!")
            messages.error(request, "Akses ditolak: Password atau header rahasia salah!")
        elif form.is_valid():
            form.save()
            messages.success(request, "Pengalaman berhasil diperbarui!")
            return redirect("main:show_experience")

    context = {
        "name": "Nashri",
        "form": form,
        "experience": experience,
    }
    return render(request, "experiences_form.html", context)

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if not is_authorized(request):
            messages.error(request, "Akses ditolak: Kode rahasia atau password salah!")
            return redirect("main:show_experience")

        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")
