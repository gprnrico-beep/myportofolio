
from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
from rest_framework import serializers

from .models import Project

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'category',
            'description',
            'star_count',
            'is_starred',
            'starred_by_names',
        ]
        read_only_fields = [
            'id',
            'star_count',
            'is_starred',
            'starred_by_names',
        ]

    def validate_title(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Project title cannot be empty."
            )

        return value

    def validate_category(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Project category cannot be empty."
            )

        return value

    def validate_description(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Project description cannot be empty."
            )

        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            return obj.starred_by.filter(
                pk=request.user.pk
            ).exists()

        return False

    def get_starred_by_names(self, obj):
        return list(
            obj.starred_by.values_list('username', flat=True)
        )
