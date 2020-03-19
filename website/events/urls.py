from django.urls import path
from .views import *
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name="events"
urlpatterns=[
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    url(r'^event/detail/(?P<event_id>\d+)/$', views.event_detail, name='event_detail'),
    #path('create/', event_create, name='event_create'),
    #path('list/',events, name='events'),
    #path('detail/<int:id>/', event_detail, name='event_detail'),
    #path('update/<int:id>/', event_update, name='event_update'),
    #path('upcoming_list/',upcoming_events, name='upcoming_events'),
    #path('',events, name='events'),
    url(r'^markdownx/', include('markdownx.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
