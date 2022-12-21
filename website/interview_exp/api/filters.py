from django_filters import rest_framework as filters
from interview_exp.models import Experiences


# need to revise the filters if needed
class ExperiencesFilter(filters.FilterSet):
    status = filters.ChoiceFilter(field_name='verification_Status', choices=Experiences.verification_Status_choices)
    role_type = filters.ChoiceFilter(field_name='role_Type', choices=Experiences.role_Type_choices)
    ctc = filters.RangeFilter(field_name='total_Compensation')

    class Meta:
        model = Experiences
        fields = {}
