from rest_framework.permissions import IsAuthenticated, BasePermission


class RevisionPermissions(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        role = user.profile.role
        if role in ('1', '2'):
            return True
        return obj.user == user
