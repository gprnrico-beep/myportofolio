
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsPortfolioOwnerOrEditorOrReadOnly


def get_projects_queryset():
    return Project.objects.prefetch_related(
        'starred_by'
    ).order_by('title', 'id')


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def project_list(request):

    if request.method == 'GET':
        queryset = get_projects_queryset()

        # Search projects by title
        search_query = request.query_params.get('title', '').strip()

        if search_query:
            queryset = queryset.filter(
                title__icontains=search_query
            )

        serializer = ProjectSerializer(
            queryset,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    # POST: Create a new project
    serializer = ProjectSerializer(
        data=request.data,
        context={'request': request}
    )

    if serializer.is_valid():
        project = serializer.save()

        return Response(
            ProjectSerializer(
                project,
                context={'request': request}
            ).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def project_detail(request, project_id):

    try:
        project = get_projects_queryset().get(id=project_id)
    except Project.DoesNotExist:
        return Response(
            {'detail': 'Project not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = ProjectSerializer(
            project,
            context={'request': request}
        )

        return Response(serializer.data)

    if request.method == 'DELETE':
        project.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    # PUT and PATCH: Update project
    partial = request.method == 'PATCH'

    serializer = ProjectSerializer(
        project,
        data=request.data,
        partial=partial,
        context={'request': request}
    )

    if serializer.is_valid():
        updated_project = serializer.save()

        return Response(
            ProjectSerializer(
                updated_project,
                context={'request': request}
            ).data,
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):

    try:
        project = get_projects_queryset().get(id=project_id)
    except Project.DoesNotExist:
        return Response(
            {'detail': 'Project not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Toggle star for the authenticated user
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)

    serializer = ProjectSerializer(
        project,
        context={'request': request}
    )

    return Response(serializer.data, status=status.HTTP_200_OK)
