import datetime
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
from main.forms import ProjectForm, ExperienceForm, SkillForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_main")
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), samesite="Lax")
        return response

    context = {
        "name": "Nashri",
        "form": form,
    }
    return render(request, "login.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Nashri",
        "form": form,
    }
    return render(request, "register.html", context)

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
        "last_login": request.COOKIES.get("last_login", "Belum ada sesi login / Cookie tidak ditemukan"),
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
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)

    context = {
        "name": "Nashri",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def show_skill(request):
    json_response = get_skills_json(request)
    skills = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills = [s.object for s in skills]
    name_query = request.GET.get("name", "").strip()

    context = {
        "name": "Nashri",
        "skill_list": skills,
        "name_query": name_query,
    }
    return render(request, "skills.html", context)

@login_required(login_url="main:login")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ProjectForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
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

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="main:login")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")

@login_required(login_url="main:login")
def update_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Proyek berhasil diperbarui!")
            return redirect("main:show_project")

    context = {
        "name": "Nashri",
        "form": form,
        "project": project,
    }
    return render(request, "projects_form.html", context)

@login_required(login_url="main:login")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        if project.starred_by.filter(pk=request.user.pk).exists():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)
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

def create_skill(request):
    form = SkillForm(request.POST or None)

    if request.method == "POST":
        if not is_authorized(request):
            form.add_error("password", "Kode rahasia atau password salah!")
            messages.error(request, "Akses ditolak: Password atau header rahasia salah!")
        elif form.is_valid():
            form.save()
            messages.success(request, "Skill baru berhasil ditambahkan!")
            return redirect("main:show_skill")

    context = {
        "name": "Nashri",
        "form": form,
    }
    return render(request, "skills_form.html", context)

def update_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    form = SkillForm(request.POST or None, instance=skill)

    if request.method == "POST":
        if not is_authorized(request):
            form.add_error("password", "Kode rahasia atau password salah!")
            messages.error(request, "Akses ditolak: Password atau header rahasia salah!")
        elif form.is_valid():
            form.save()
            messages.success(request, "Skill berhasil diperbarui!")
            return redirect("main:show_skill")

    context = {
        "name": "Nashri",
        "form": form,
        "skill": skill,
    }
    return render(request, "skills_form.html", context)

def get_skills_json(request):
    name_query = request.GET.get("name", "").strip()
    skills = Skill.objects.all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)

    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")

def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        if not is_authorized(request):
            messages.error(request, "Akses ditolak: Kode rahasia atau password salah!")
            return redirect("main:show_skill")

        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skill")

    return redirect("main:show_skill")
