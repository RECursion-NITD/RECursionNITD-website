from rest_framework.permissions import BasePermission, SAFE_METHODS


class MembersListCreatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        role = request.user.profile.role
        return role in ('1', '2')
