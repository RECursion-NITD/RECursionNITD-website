"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls import url, include
from forum import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from user_profile.api.views import MyTokenObtainPairView

urlpatterns = [

                  path('admin/', admin.site.urls),
                  path('', views.home, name='home'),
                  path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('oauth/', include('social_django.urls', namespace='social')),
                  path('forum/', include('forum.urls', namespace='forum')),
                  # path('events/',include('events.urls',namespace='events')),
                  path('events/', include('events_calendar.urls', namespace='events_calendar')),
                  path('profile/', include('user_profile.urls', namespace='user_profile')),
                  path('team/', include('team.urls', namespace='team')),
                  path('blog/', include('blog.urls', namespace='blog')),
                  path('experience/', include('interview_exp.urls', namespace='interview_exp')),
                  path('get_started/', include('getting_started.urls', namespace='getting_started')),
                  # path('members/',include('members.urls')),
                  url(r'^markdownx/', include('markdownx.urls')),

                  # API region

                  # API URLs
                  path('api/users/', include('user_profile.api.urls', namespace='user_profile_api')),
                  path('api/experiences/', include('interview_exp.api.urls', namespace='experiences_api')),
                  path('api/events/', include('events_calendar.api.urls', namespace='events_api')),
                  path('api/team/', include('team.api.urls', namespace='team_api')),

                  # JWT
                  path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  # Prometheus monitoring
                  path('', include('django_prometheus.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
