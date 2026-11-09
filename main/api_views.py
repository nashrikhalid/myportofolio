from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import Project, Experience, Skill
from main.serializers import ProjectSerializer, ExperienceSerializer, SkillSerializer
from main.permissions import IsPortfolioOwnerOrReadOnly, IsPortfolioOwnerOrEditorOrReadOnly


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    if request.method in ("GET", "HEAD"):
        objects = Project.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            objects = objects.filter(title__icontains=title)
        return Response(ProjectSerializer(objects, many=True, context={"request": request}).data)
    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=201)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    obj = get_object_or_404(Project.objects.prefetch_related("starred_by"), pk=project_id)
    if request.method in ("GET", "HEAD"):
        return Response(ProjectSerializer(obj, context={"request": request}).data)
    if request.method == "DELETE":
        obj.delete()
        return Response(status=204)
    serializer = ProjectSerializer(obj, data=request.data, partial=request.method == "PATCH", context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    obj = get_object_or_404(Project, pk=project_id)
    if obj.starred_by.filter(pk=request.user.pk).exists():
        obj.starred_by.remove(request.user)
    else:
        obj.starred_by.add(request.user)
    return Response(ProjectSerializer(obj, context={"request": request}).data)


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    if request.method in ("GET", "HEAD"):
        objects = Experience.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            objects = objects.filter(title__icontains=title)
        return Response(ExperienceSerializer(objects, many=True, context={"request": request}).data)
    serializer = ExperienceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=201)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    obj = get_object_or_404(Experience.objects.prefetch_related("starred_by"), pk=experience_id)
    if request.method in ("GET", "HEAD"):
        return Response(ExperienceSerializer(obj, context={"request": request}).data)
    if request.method == "DELETE":
        obj.delete()
        return Response(status=204)
    serializer = ExperienceSerializer(obj, data=request.data, partial=request.method == "PATCH", context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    obj = get_object_or_404(Experience, pk=experience_id)
    if obj.starred_by.filter(pk=request.user.pk).exists():
        obj.starred_by.remove(request.user)
    else:
        obj.starred_by.add(request.user)
    return Response(ExperienceSerializer(obj, context={"request": request}).data)


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_list(request):
    if request.method in ("GET", "HEAD"):
        skills = Skill.objects.order_by("name", "id")
        name = request.query_params.get("name", "").strip()
        if name:
            skills = skills.filter(name__icontains=name)
        return Response(SkillSerializer(skills, many=True).data)
    serializer = SkillSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=201)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_detail(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    if request.method in ("GET", "HEAD"):
        return Response(SkillSerializer(skill).data)
    if request.method == "DELETE":
        skill.delete()
        return Response(status=204)
    serializer = SkillSerializer(skill, data=request.data, partial=request.method == "PATCH")
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
