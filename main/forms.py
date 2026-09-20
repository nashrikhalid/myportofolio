from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput, PasswordInput, Select, DateInput

from main.models import Project, Skill, Experience

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
    )

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

class ExperienceForm(ModelForm):
    password = forms.CharField(
        widget=PasswordInput(
            attrs={
                "placeholder": "Masukkan kode rahasia / password",
                "autocomplete": "current-password",
            }
        ),
        label="Password Rahasia",
        required=False,
    )
    class Meta:
        model = Experience
        fields = [
            "title",
            "org",
            "description",
            "category",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Pengalaman",
            "org": "Organisasi/Instansi",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori Pengalaman",
            "started_at": "Waktu mulai",
            "ended_at": "Waktu berakhir",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Pengalaman",
                    "maxlength": 255,
                }
            ),
            "org": TextInput(
                attrs={
                    "placeholder": "Fasilkom UI",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Apa yang kamu dapatkan dari pengalaman ini?",
                    "rows": 3,
                }
            ),
            "category": Select(),
            "started_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

class SkillForm(ModelForm):
    password = forms.CharField(
        widget=PasswordInput(
            attrs={
                "placeholder": "Masukkan kode rahasia / password",
                "autocomplete": "current-password",
            }
        ),
        label="Password Rahasia",
        required=False,
    )
    class Meta:
        model = Skill
        fields = [
            "name",
            "logo",
        ]

        labels = {
            "name": "Nama Skill/Tool",
            "logo": "Logo",
        }

        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "Python, Java, etc",
                    "maxlength": 255,
                }
            ),
            "logo": TextInput(
                attrs={
                    "placeholder": "fa-brands fa-python (Font Awesome) atau URL gambar",
                    "maxlength": 100,
                }
            ),
        }