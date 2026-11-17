
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedEditorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        if request.method == "DELETE":
            return request.user.is_staff

        return True
