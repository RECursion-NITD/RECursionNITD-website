from django_filters import rest_framework as filters
from team.models import Members


class MembersFilter(filters.FilterSet):
    batch_year = filters.NumberFilter(field_name='batch_year', label='batch')

    class Meta:
        model = Members
        fields = ['batch_year', ]
