from django.shortcuts import render

from django.shortcuts import render

from main.models import Experience


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
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Nashri",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
