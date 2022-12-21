from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission
from user_profile.models import Profile


class ViewUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS) or bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated) and request.user == obj.user


class IsMemberOrAbove(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        curr_user = request.user
        curr_profile = Profile.objects.get(user=curr_user)
        return curr_profile.role != '3'
