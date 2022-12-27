from django_filters import rest_framework as filters
from events_calendar.models import Events_Calendar


class EventsFilter(filters.FilterSet):
    event_type = filters.ChoiceFilter(field_name='event_type', choices=Events_Calendar.event_choices)
    target_year = filters.ChoiceFilter(field_name='target_year', choices=Events_Calendar.year_choices)

    class Meta:
        model = Events_Calendar
        fields = {
            'start_time': ['gte', 'lte'],
            'end_time': ['gte', 'lte'],
        }
