from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response

from django.utils import timezone
import datetime
from events_calendar.api.serializers import EventsSerializer, Events_Calendar
# from events_calendar.models import Events_Calendar
from user_profile.models import User, Profile
from user_profile.api.serializers import ProfileSerializer, UserSerializer


@api_view(['GET', ])
def home_view(request) -> Response:
    data = {}
    user = request.user
    max_events = 4
    if user.is_authenticated:
        data['user_profile'] = ProfileSerializer(Profile.objects.get(user=user),
                                                 context={'request': request}).data
    else:
        data['user_profile'] = {}

    today = timezone.now()
    founding_date = datetime.datetime(2014, 9, 1, 00, 00, tzinfo=today.tzinfo)
    data['years_of_experience'] = (today - founding_date).days // 365  # roughly
    upcoming_events = Events_Calendar.objects.filter(
        start_time__range=[today, today + datetime.timedelta(days=7)]
    )[:max_events]  # expects QS to be sorted by start date
    data['upcoming_events'] = EventsSerializer(upcoming_events, many=True, context={'request': request}).data
    data['hours_teaching'] = 300 + Events_Calendar.objects.filter(event_type='Class').count() * 2
    data['contest_count'] = 40 + Events_Calendar.objects.filter(event_type='Contest').count()
    return Response(data=data)
