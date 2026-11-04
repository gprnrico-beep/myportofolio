
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    Allow everyone to read projects.
    Only superusers can create and delete projects.
    Superusers and users in the Editor group can update projects.
    """

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        # Everyone can perform safe methods (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # User must be authenticated
        if not request.user.is_authenticated:
            return False

        # Superuser can perform all actions
        if request.user.is_superuser:
            return True

        # Editor can only update projects
        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )
