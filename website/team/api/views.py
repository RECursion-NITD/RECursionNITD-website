from django_filters import rest_framework as filters
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from team.models import Members
from .serilazers import MemberSerializer
from .permissions import MembersListCreatePermission
from .filters import MembersFilter

from rest_framework import generics
from team.models import Members
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters
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




class AlumniYearWiseView(generics.ListAPIView):
    serializer_class = MemberSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MembersFilter

    def get_queryset(self):
        year = self.request.query_params.get('year', None)
        if year:
            return Members.objects.filter(batch_year=year).order_by('-batch_year', 'name')
        return Members.objects.all().order_by('-batch_year', 'name')  # Default to all alumni if no year is specified

