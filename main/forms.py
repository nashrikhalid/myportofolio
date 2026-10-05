from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput, DateTimeField

from main.models import Project, Skill, Experience

from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class ProjectForm(ModelForm):
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
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class ExperienceForm(ModelForm):
    started_at = DateTimeField(
        label="Bulan dan tahun mulai",
        input_formats=["%Y-%m"],
        widget=DateInput(format="%Y-%m", attrs={"type": "month"}),
    )
    ended_at = DateTimeField(
        label="Bulan dan tahun berakhir",
        required=False,
        input_formats=["%Y-%m"],
        widget=DateInput(format="%Y-%m", attrs={"type": "month"}),
        help_text="Kosongkan jika pengalaman masih berlangsung.",
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
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama pengalaman tidak boleh hanya berisi tag HTML.")
        return title

    def clean_org(self):
        org = strip_tags(self.cleaned_data["org"]).strip()
        if not org:
            raise ValidationError("Organisasi tidak boleh kosong atau hanya berisi tag HTML.")
        return org

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class SkillForm(ModelForm):
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
