from django.urls import path
from .views import *
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static

app_name="experience"
urlpatterns = [
      path('add', add_experience, name='add_experience'),
      path('update/<int:id>/', update_experience, name='update_experience'),
      path('', list_experiences, name='list_experiences'),
      path('search/<str:key>', search_experience, name='search_experience'),
      path('filter/<str:role>', filter_experience, name='filter_experience'),
      path('detail/<int:id>/', detail_experiences, name='detail_experiences'),
      path('revise/<int:id>/<str:action>', revise_experience, name='revise_experience'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)