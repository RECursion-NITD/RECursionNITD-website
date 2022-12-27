from django_filters import rest_framework as filters
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from team.models import Members
from .serilazers import MemberSerializer
from .permissions import MembersListCreatePermission
from .filters import MembersFilter


# SCOPE FOR CACHING #

class ListCreateMembersView(ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = (MembersListCreatePermission,)
    pagination_class = None
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
    filterset_class = MembersFilter
    search_fields = ['name', 'branch', 'designation']
    ordering_fields = ['batch_year', 'name', 'designation', 'branch']

    def get_queryset(self):
        return Members.objects.all()
