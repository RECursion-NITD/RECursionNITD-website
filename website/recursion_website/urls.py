from . import views
from django.conf.urls import include,url
from django.conf import settings
from django.urls import path


urlpatterns = [
               
                url(r'add_question/$',views.add_question,name = 'add_question'),
                path('',views.questions,name='questions'),
               
              ]