from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_project,
    show_skill,
    create_project,
    update_project,
    delete_project,
    get_projects_json,
    create_experience,
    update_experience,
    delete_experience,
    get_experiences_json,
    create_skill,
    update_skill,
    delete_skill,
    get_skills_json,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", show_project, name="show_project"),
    path("skill/", show_skill, name="show_skill"),
    # Projects
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/edit/", update_project, name="update_project"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    # Experiences
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    # Skills
    path("skill/add/", create_skill, name="create_skill"),
    path("skill/<uuid:skill_id>/edit/", update_skill, name="update_skill"),
    path("skill/<uuid:skill_id>/delete/", delete_skill, name="delete_skill"),
    path("api/skills/", get_skills_json, name="get_skills_json"),
]