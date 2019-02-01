from django.urls import path
from .views import *
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('list/',events, name='events'),
    path('detail/<int:id>/', event_detail, name='event_detail'),
    path('update/<int:id>/', event_update, name='event_update'),
    path('upcoming_list/',upcoming_events, name='upcoming_events'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
