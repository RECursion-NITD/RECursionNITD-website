from django.urls import path
from .views import *
from django.urls import include, re_path
from django.conf import settings
from django.conf.urls.static import static

app_name="events"
urlpatterns=[
    path('create/', event_create, name='event_create'),
    path('list/',events, name='events'),
    path('detail/<int:event_id>/', event_detail, name='event_detail'),
    path('calender/', calender, name='calender'),
    path('update/<int:event_id>/', event_update, name='event_update'),
    path('upcoming_list/',upcoming_events, name='upcoming_events'),
    path('',events, name='events'),
    re_path(r'^markdownx/', include('markdownx.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
