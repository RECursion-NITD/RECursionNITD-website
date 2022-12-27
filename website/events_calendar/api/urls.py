from django.urls import path

from .views import (
    EventsListCreateView,
    EventsRetrieveUpdateDestroyView,

)

app_name = 'events_api'

urlpatterns = [
    path('', EventsListCreateView.as_view(), name='events_list'),
    path('<int:slug>/', EventsRetrieveUpdateDestroyView.as_view(), name='events_detail'),
]
