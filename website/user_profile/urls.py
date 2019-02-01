from django.urls import path
from .views import *
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('viewprofile/<int:id>/', view_profile, name='view_profile'),
    path('register/', user_register, name="user_register"),
    path('editprofile/', edit_profile, name='edit_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
