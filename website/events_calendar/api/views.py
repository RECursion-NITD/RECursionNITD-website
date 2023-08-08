from django_filters import rest_framework as filters

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from events_calendar.models import Events_Calendar
from events_calendar.views import get_event_duration
from .serializers import EventsSerializer
from .permissions import EventsListCreatePermission, EventRetrieveUpdateDestroyPermission
from .filters import EventsFilter


# HIGH POTENTIAL FOR CACHING

class EventsListCreateView(ListCreateAPIView):
    serializer_class = EventsSerializer
    permission_classes = (EventsListCreatePermission,)
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = EventsFilter
    search_fields = ['title', 'description', 'venue']
    ordering_fields = ['start_time', 'end_time', 'updated_at', 'duration']

    def get_queryset(self):
        return Events_Calendar.objects.select_related('user').all()

    def perform_create(self, serializer):
        start_time, end_time = serializer.validated_data.get('start_time'), serializer.validated_data.get('end_time')
        serializer.save(user=self.request.user, duration=get_event_duration(start_time, end_time))


class EventsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventsSerializer
    permission_classes = (EventRetrieveUpdateDestroyPermission,)
    lookup_field = 'id'
    lookup_url_kwarg = 'slug'

    def get_queryset(self):
        return Events_Calendar.objects.select_related('user').all()

    def perform_update(self, serializer):
        # Saving twice. Need to find a better way to do it
        # Preferably using pre_save signals
        event = serializer.save()
        event.duration = get_event_duration(event.start_time, event.end_time)
        event.save()
