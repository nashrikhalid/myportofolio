from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput, PasswordInput

from main.models import Project

class ProjectForm(ModelForm):
    password = forms.CharField(
        widget=PasswordInput(
            attrs={
                "placeholder": "Masukkan kode rahasia / password",
                "autocomplete": "current-password",
            }
        ),
        label="Password Rahasia",
        required=False,
        help_text="Masukkan kode rahasia yang terdaftar di .env",
    )

    field_order = [
        "title",
        "description",
        "tech_stack",
        "project_url",
        "project_image_url",
        "password",
    ]

    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }