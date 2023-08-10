from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS


class EventsListCreatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        role = request.user.profile.role
        return role in ('1', '2')


class EventRetrieveUpdateDestroyPermission(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not bool(request.user and request.user.is_authenticated):
            return False
        role = request.user.profile.role
        return role in ('1', '2')

