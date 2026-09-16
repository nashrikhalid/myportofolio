from django.shortcuts import render
from main.models import Experience
from main.models import Project
from main.models import Skill
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from main.forms import ProjectForm


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
    context = {
        "name": "Nashri",
        "experience_list": Experience.objects.all(),
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

    if request.method == "POST" and form.is_valid():
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
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")
