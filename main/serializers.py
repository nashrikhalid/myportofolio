from django.utils.html import strip_tags
from rest_framework import serializers
from main.models import Project, Experience, Skill


class StarredSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        return bool(request and request.user.is_authenticated and request.user in obj.starred_by.all())

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)


class ProjectSerializer(StarredSerializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    tech_stack = serializers.CharField(max_length=255)

    class Meta:
        model = Project
        fields = ["id", "title", "description", "tech_stack", "project_url",
                  "project_image_url", "star_count", "is_starred", "starred_by_names"]
        read_only_fields = ["id"]

    def validate_tech_stack(self, value):
        return strip_tags(value)


class ExperienceSerializer(StarredSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    started_at = serializers.DateTimeField(input_formats=["iso-8601", "%Y-%m"])
    ended_at = serializers.DateTimeField(input_formats=["iso-8601", "%Y-%m"], allow_null=True, required=False)

    class Meta:
        model = Experience
        fields = ["id", "title", "org", "description", "category", "category_display",
                  "started_at", "ended_at", "is_ongoing", "star_count", "is_starred", "starred_by_names"]
        read_only_fields = ["id", "is_ongoing"]

    def validate_org(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Organization cannot be empty.")
        return value


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "logo"]
        read_only_fields = ["id"]

    def validate_name(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama skill tidak boleh kosong.")
        return value

    def validate_logo(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Logo skill tidak boleh kosong.")
        return value
