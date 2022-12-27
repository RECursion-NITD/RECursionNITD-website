from rest_framework import serializers

from events_calendar.models import Events_Calendar
from user_profile.api.serializers import UserSerializer


class EventsSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='events_api:events_detail', lookup_field='id',
                                               lookup_url_kwarg='slug')
    user = UserSerializer(read_only=True)

    class Meta:
        model = Events_Calendar
        # exclude = ['id', ]
        fields = '__all__'
        read_only_fields = ['user', 'url', 'duration', ]
